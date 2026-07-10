import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdtemp, readFile, rm, stat } from "node:fs/promises";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { extname, join, resolve, sep } from "node:path";

if (typeof WebSocket !== "function") {
  throw new Error("This browser regression requires Node 24 or newer");
}

const SITE_ROOT = resolve("site");
const MOBILE_WIDTH = 390;
const MOBILE_HEIGHT = 844;
const MIME_TYPES = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
};

const delay = (milliseconds) =>
  new Promise((resolveDelay) => setTimeout(resolveDelay, milliseconds));

const findChrome = () => {
  const candidates = [
    process.env.CHROME_BIN,
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ].filter(Boolean);
  const executable = candidates.find((candidate) => existsSync(candidate));
  if (!executable) {
    throw new Error(`Chrome not found; checked: ${candidates.join(", ")}`);
  }
  return executable;
};

const startSiteServer = async () => {
  const server = createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(
        new URL(request.url ?? "/", "http://127.0.0.1").pathname,
      );
      let filePath = resolve(SITE_ROOT, `.${pathname}`);
      if (filePath !== SITE_ROOT && !filePath.startsWith(`${SITE_ROOT}${sep}`)) {
        response.writeHead(403).end("Forbidden");
        return;
      }
      if ((await stat(filePath)).isDirectory()) filePath = join(filePath, "index.html");
      const body = await readFile(filePath);
      response.writeHead(200, {
        "content-type": MIME_TYPES[extname(filePath)] ?? "application/octet-stream",
      });
      response.end(body);
    } catch {
      response.writeHead(404).end("Not found");
    }
  });
  await new Promise((resolveListen) => server.listen(0, "127.0.0.1", resolveListen));
  const address = server.address();
  assert(address && typeof address === "object");
  return { server, url: `http://127.0.0.1:${address.port}/` };
};

const waitForDebugUrl = (chrome) =>
  new Promise((resolveDebugUrl, rejectDebugUrl) => {
    let output = "";
    const timeout = setTimeout(
      () => rejectDebugUrl(new Error(`Chrome did not expose CDP:\n${output}`)),
      15_000,
    );
    chrome.stderr.on("data", (chunk) => {
      output += chunk.toString();
      const match = output.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (!match) return;
      clearTimeout(timeout);
      resolveDebugUrl(match[1]);
    });
    chrome.once("exit", (code) => {
      clearTimeout(timeout);
      rejectDebugUrl(new Error(`Chrome exited before CDP was ready: ${code}\n${output}`));
    });
  });

const connectCdp = async (webSocketUrl) => {
  const socket = new WebSocket(webSocketUrl);
  await new Promise((resolveOpen, rejectOpen) => {
    socket.addEventListener("open", resolveOpen, { once: true });
    socket.addEventListener("error", rejectOpen, { once: true });
  });

  let commandId = 0;
  const pending = new Map();
  const listeners = new Map();
  socket.addEventListener("message", ({ data }) => {
    const message = JSON.parse(data);
    if (message.id && pending.has(message.id)) {
      const { resolveCommand, rejectCommand } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) rejectCommand(new Error(JSON.stringify(message.error)));
      else resolveCommand(message.result ?? {});
      return;
    }
    for (const listener of listeners.get(message.method) ?? []) listener(message.params);
  });

  const send = (method, params = {}) =>
    new Promise((resolveCommand, rejectCommand) => {
      const id = ++commandId;
      pending.set(id, { resolveCommand, rejectCommand });
      socket.send(JSON.stringify({ id, method, params }));
    });

  const once = (method) =>
    new Promise((resolveEvent) => {
      const listener = (params) => {
        listeners.set(
          method,
          (listeners.get(method) ?? []).filter((candidate) => candidate !== listener),
        );
        resolveEvent(params);
      };
      listeners.set(method, [...(listeners.get(method) ?? []), listener]);
    });

  return { send, once, close: () => socket.close() };
};

const evaluate = async (cdp, expression) => {
  const response = await cdp.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (response.exceptionDetails) {
    throw new Error(response.exceptionDetails.text ?? "Browser evaluation failed");
  }
  return response.result.value;
};

const poll = async (cdp, expression, description) => {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    if (await evaluate(cdp, expression)) return;
    await delay(25);
  }
  throw new Error(`Timed out waiting for ${description}`);
};

const press = async (cdp, key, { shift = false } = {}) => {
  const params = {
    key,
    code: key === "Tab" ? "Tab" : "Escape",
    windowsVirtualKeyCode: key === "Tab" ? 9 : 27,
    nativeVirtualKeyCode: key === "Tab" ? 9 : 27,
    modifiers: shift ? 8 : 0,
  };
  await cdp.send("Input.dispatchKeyEvent", { ...params, type: "keyDown" });
  await cdp.send("Input.dispatchKeyEvent", { ...params, type: "keyUp" });
  await delay(50);
};

const stateExpression = `(() => ({
  open: document.querySelector("#__search").checked,
  expanded: document.querySelector(".ds-search-toggle").getAttribute("aria-expanded"),
  activeClass: document.activeElement.className,
  activeComponent: document.activeElement.getAttribute("data-md-component"),
  insideDialog: document.querySelector("#__search-dialog").contains(document.activeElement)
}))()`;

const userDataDirectory = await mkdtemp(join(tmpdir(), "ds-python101-chrome-"));
const { server, url } = await startSiteServer();
const chrome = spawn(
  findChrome(),
  [
    "--headless=new",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--no-sandbox",
    "--remote-debugging-port=0",
    `--user-data-dir=${userDataDirectory}`,
    `--window-size=${MOBILE_WIDTH},${MOBILE_HEIGHT}`,
    "about:blank",
  ],
  { stdio: ["ignore", "ignore", "pipe"] },
);
const chromeExited = new Promise((resolveExit) => chrome.once("exit", resolveExit));

let cdp;
try {
  const debugUrl = new URL(await waitForDebugUrl(chrome));
  const target = await fetch(
    `http://${debugUrl.host}/json/new?${encodeURIComponent("about:blank")}`,
    { method: "PUT" },
  ).then((response) => response.json());
  cdp = await connectCdp(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: MOBILE_WIDTH,
    height: MOBILE_HEIGHT,
    deviceScaleFactor: 1,
    mobile: true,
    screenWidth: MOBILE_WIDTH,
    screenHeight: MOBILE_HEIGHT,
  });
  const loaded = cdp.once("Page.loadEventFired");
  await cdp.send("Page.navigate", { url });
  await loaded;
  await poll(
    cdp,
    `document.readyState === "complete" &&
      document.querySelector(".ds-search-toggle") &&
      document.querySelector("#__search-dialog").inert`,
    "the mobile shell to initialize",
  );

  await evaluate(cdp, `document.querySelector(".ds-search-toggle").click()`);
  await poll(
    cdp,
    `document.querySelector("#__search").checked &&
      document.activeElement.matches('[data-md-component="search-query"]')`,
    "search to open and focus its query",
  );

  await press(cdp, "Tab");
  let state = await evaluate(cdp, stateExpression);
  assert.equal(state.open, true, "Tab must not close mobile search");
  assert.equal(state.expanded, "true");
  assert.equal(state.insideDialog, true);
  assert.match(state.activeClass, /ds-search-close/);

  await evaluate(
    cdp,
    `document.querySelector('[data-md-component="search-query"]').focus()`,
  );
  await press(cdp, "Tab", { shift: true });
  state = await evaluate(cdp, stateExpression);
  assert.equal(state.open, true, "Shift+Tab must not close mobile search");
  assert.equal(state.insideDialog, true);
  assert.match(state.activeClass, /md-search__scrollwrap/);

  await press(cdp, "Tab");
  state = await evaluate(cdp, stateExpression);
  assert.equal(state.open, true, "wrapped Tab must keep mobile search open");
  assert.equal(state.activeComponent, "search-query");

  await press(cdp, "Escape");
  state = await evaluate(cdp, stateExpression);
  assert.equal(state.open, false);
  assert.equal(state.expanded, "false");
  assert.match(state.activeClass, /ds-search-toggle/);

  console.log("Mobile search keyboard focus regression passed");
} finally {
  cdp?.close();
  if (chrome.exitCode === null) chrome.kill("SIGTERM");
  await Promise.race([chromeExited, delay(5_000)]);
  if (chrome.exitCode === null) {
    chrome.kill("SIGKILL");
    await chromeExited;
  }
  await new Promise((resolveClose) => server.close(resolveClose));
  await rm(userDataDirectory, {
    force: true,
    maxRetries: 10,
    recursive: true,
    retryDelay: 100,
  });
}
