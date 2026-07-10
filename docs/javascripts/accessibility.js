(() => {
  "use strict";

  const drawerQuery = window.matchMedia("(max-width: 76.234375em)");
  const searchQuery = window.matchMedia("(max-width: 59.984375em)");
  const lastTrigger = { drawer: null, search: null };
  let shellReady = false;

  const getToggle = (name) =>
    document.querySelector(`[data-md-toggle="${name}"]`);

  const focusWithoutScroll = (element) => {
    if (!element || typeof element.focus !== "function") return;
    element.focus({ preventScroll: true });
  };

  const setInteractive = (element, enabled) => {
    if (!element) return;
    element.toggleAttribute("inert", !enabled);
    element.setAttribute("aria-hidden", String(!enabled));
  };

  const syncShell = () => {
    const drawer = getToggle("drawer");
    const search = getToggle("search");
    const navigation = document.querySelector("#site-navigation");
    const searchDialog = document.querySelector("#__search-dialog");
    const drawerOpen = Boolean(drawer?.checked);
    const searchOpen = Boolean(search?.checked);

    document.querySelectorAll('[data-ds-toggle="drawer"]').forEach((button) => {
      button.setAttribute("aria-expanded", String(drawerOpen));
      button.setAttribute(
        "aria-label",
        drawerOpen ? "Close navigation" : "Open navigation",
      );
    });

    document.querySelectorAll('[data-ds-toggle="search"]').forEach((button) => {
      const isDialogButton = button.closest("#__search-dialog");
      if (!isDialogButton) {
        button.setAttribute("aria-expanded", String(searchOpen));
      }
      button.setAttribute(
        "aria-label",
        searchOpen ? "Close search" : "Open search",
      );
    });

    if (navigation) {
      setInteractive(navigation, !drawerQuery.matches || drawerOpen);
    }

    if (searchDialog) {
      setInteractive(searchDialog, !searchQuery.matches || searchOpen);
      searchDialog.setAttribute(
        "aria-modal",
        String(searchQuery.matches && searchOpen),
      );
    }
  };

  const restoreFocus = (name) => {
    if (name === "search" && !searchQuery.matches) {
      focusWithoutScroll(
        document.querySelector('[data-md-component="search-query"]'),
      );
      return;
    }

    const selector =
      name === "drawer"
        ? ".ds-drawer-toggle"
        : ".ds-search-toggle";
    const fallback = document.querySelector(selector);
    const trigger = lastTrigger[name];
    focusWithoutScroll(trigger?.isConnected ? trigger : fallback);
  };

  const setOpen = (name, open, trigger) => {
    const toggle = getToggle(name);
    if (!toggle || toggle.checked === open) return;

    if (open) {
      lastTrigger[name] = trigger;
      const otherName = name === "drawer" ? "search" : "drawer";
      const otherToggle = getToggle(otherName);
      if (otherToggle?.checked) {
        restoreFocus(otherName);
        otherToggle.click();
      }
    } else {
      restoreFocus(name);
    }

    toggle.click();
    syncShell();

    if (!open) return;
    window.requestAnimationFrame(() => {
      const target =
        name === "drawer"
          ? document.querySelector("#site-navigation .ds-nav-close")
          : document.querySelector('[data-md-component="search-query"]');
      focusWithoutScroll(target);
    });
  };

  const visibleFocusable = (container) =>
    Array.from(
      container.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]:not([tabindex="-1"])',
      ),
    ).filter(
      (element) =>
        !element.hasAttribute("hidden") && element.getClientRects().length > 0,
    );

  const trapSearchFocus = (event) => {
    if (event.key !== "Tab" || !searchQuery.matches) return;
    const search = getToggle("search");
    const dialog = document.querySelector("#__search-dialog");
    if (!search?.checked || !dialog) return;

    const focusable = visibleFocusable(dialog);
    if (!focusable.length) return;
    const currentIndex = focusable.indexOf(document.activeElement);
    const nextIndex =
      currentIndex < 0
        ? event.shiftKey
          ? focusable.length - 1
          : 0
        : (currentIndex + (event.shiftKey ? -1 : 1) + focusable.length) %
          focusable.length;

    // Material closes mobile search during its own Tab handling. Intercept the
    // key before it reaches that handler and move focus within the dialog.
    event.preventDefault();
    event.stopPropagation();
    focusWithoutScroll(focusable[nextIndex]);
  };

  const addMediaListener = (query) => {
    if (typeof query.addEventListener === "function") {
      query.addEventListener("change", syncShell);
    } else {
      query.addListener(syncShell);
    }
  };

  const initShell = () => {
    if (shellReady) return;
    shellReady = true;

    document.addEventListener("click", (event) => {
      const toggleButton = event.target.closest("[data-ds-toggle]");
      if (toggleButton) {
        event.preventDefault();
        const name = toggleButton.dataset.dsToggle;
        const toggle = getToggle(name);
        setOpen(name, !toggle?.checked, toggleButton);
        return;
      }

      const closeButton = event.target.closest("[data-ds-close]");
      if (closeButton) {
        event.preventDefault();
        setOpen(closeButton.dataset.dsClose, false, closeButton);
      }
    });

    document.addEventListener(
      "keydown",
      (event) => {
        trapSearchFocus(event);
        if (event.defaultPrevented || event.key !== "Escape") return;

        if (getToggle("search")?.checked) {
          event.preventDefault();
          setOpen("search", false, document.activeElement);
        } else if (getToggle("drawer")?.checked) {
          event.preventDefault();
          setOpen("drawer", false, document.activeElement);
        }
      },
      { capture: true },
    );

    ["drawer", "search"].forEach((name) => {
      getToggle(name)?.addEventListener("change", (event) => {
        if (!event.currentTarget.checked) {
          const controlled =
            name === "drawer"
              ? document.querySelector("#site-navigation")
              : document.querySelector("#__search-dialog");
          if (controlled?.contains(document.activeElement)) restoreFocus(name);
        }
        syncShell();
      });
    });
    addMediaListener(drawerQuery);
    addMediaListener(searchQuery);
    syncShell();
  };

  const cleanHeadingText = (heading) =>
    heading?.textContent.replace(/[\u00b6#]\s*$/, "").trim();

  const tableLabel = (table, index) => {
    const article = table.closest("article") || document.body;
    const headings = Array.from(
      article.querySelectorAll("h1, h2, h3, h4, h5, h6"),
    ).filter(
      (heading) =>
        heading.compareDocumentPosition(table) & Node.DOCUMENT_POSITION_FOLLOWING,
    );
    return cleanHeadingText(headings.at(-1)) || `Data table ${index + 1}`;
  };

  const updateTableState = (region) => {
    const shell = region.closest(".ds-table-shell");
    if (!shell) return;
    const overflow = region.scrollWidth - region.clientWidth > 2;
    const atEnd =
      !overflow || region.scrollLeft + region.clientWidth >= region.scrollWidth - 2;
    shell.dataset.overflow = String(overflow);
    shell.dataset.atEnd = String(atEnd);
    region.tabIndex = overflow ? 0 : -1;
    if (overflow) {
      region.setAttribute("role", "region");
    } else {
      region.removeAttribute("role");
    }
  };

  const enhanceTables = (root = document) => {
    root.querySelectorAll(".md-typeset table:not([class])").forEach((table, index) => {
      if (table.closest(".ds-table-region")) return;

      const label = tableLabel(table, index);
      let caption = table.querySelector(":scope > caption");
      if (!caption) {
        caption = document.createElement("caption");
        caption.className = "ds-visually-hidden";
        caption.textContent = `${label} table`;
        table.prepend(caption);
      }
      caption.id ||= `ds-table-caption-${index + 1}`;

      const shell = document.createElement("div");
      shell.className = "ds-table-shell";
      shell.dataset.overflow = "false";
      shell.dataset.atEnd = "true";

      const hint = document.createElement("p");
      hint.className = "ds-table-hint";
      hint.id = `ds-table-hint-${index + 1}`;
      hint.textContent = "Scroll horizontally to see every column →";

      const region = document.createElement("div");
      region.className = "ds-table-region";
      region.tabIndex = -1;
      region.setAttribute("aria-labelledby", caption.id);
      region.setAttribute("aria-describedby", hint.id);

      table.before(shell);
      shell.append(hint, region);
      region.append(table);
      table.dataset.columns = String(
        table.querySelectorAll(":scope > thead > tr:first-child > th").length,
      );

      region.addEventListener("scroll", () => updateTableState(region), {
        passive: true,
      });
      if ("ResizeObserver" in window) {
        const observer = new ResizeObserver(() => updateTableState(region));
        observer.observe(region);
        observer.observe(table);
        shell.dsResizeObserver = observer;
      }
      updateTableState(region);
    });
  };

  const init = () => {
    initShell();
    enhanceTables();
  };

  init();
  if (typeof document$ !== "undefined") {
    document$.subscribe(() => enhanceTables());
  }
})();
