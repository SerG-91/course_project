import os

import pytest

from config import ROOT_PATH


@pytest.fixture
def path():
    DATA_PATH = os.path.join(ROOT_PATH, "data")
    path_df = os.path.join(DATA_PATH, "operations.xlsx")
    return path_df
