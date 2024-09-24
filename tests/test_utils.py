from unittest.mock import Mock, patch

import pandas as pd

from src.utils import get_data_info


@patch("pd.read_excel")
def test_get_data_info(path, mock_random):
    mock_random.return_value = 5
    assert get_data_info(path) == 5
