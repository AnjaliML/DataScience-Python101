from pathlib import Path

import pandas as pd
import pytest

from ds_python101.data import load_customer_data

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_renewals.csv"


@pytest.fixture
def customers() -> pd.DataFrame:
    return load_customer_data(DATA_PATH)
