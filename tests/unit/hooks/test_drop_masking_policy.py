from dataclasses import dataclass
from unittest import mock

import pytest

from sqlmeshsm.hooks import drop_masking_policy


@dataclass
class SFResultMaskingPolicyRef:
    materialization: str = "table"
    model: str = "my_model"
    column: str = "my_column"


class TestDropMaskingPolicy:
    @pytest.mark.parametrize(
        "mock_from_records_rv",
        [([]), ([SFResultMaskingPolicyRef()])],
    )
    @mock.patch("sqlmeshsm.hooks.drop_masking_policy.DataFrame.from_records")
    @mock.patch("snowflake.connector.connect")
    @mock.patch("sqlmeshsm.hooks.helper.SQLQuery.take")
    @mock.patch("builtins.open", mock.mock_open(read_data="data: data"))
    def test_drop_masking_policy(
        self,
        mock_SQLQuery_take,
        mock_connector_connect,
        mock_from_records,
        mock_from_records_rv,
    ):
        mock_from_records.return_value = mock_from_records_rv
        _ = drop_masking_policy.drop_masking_policy(
            mp_func_name="dummy", config_path="dummy"
        )
        calls = [
            mock.call("fetch_masking_policy_references", **dict(mp_func_name="dummy")),
            mock.call("drop_masking_policy", **dict(mp_func_name="dummy")),
        ]
        mock_SQLQuery_take.assert_has_calls(
            calls, any_order=(len(mock_from_records_rv) != 0)
        )
        mock_connector_connect.assert_called_once_with(**dict(data="data"))
        if mock_from_records_rv:
            assert mock_from_records.call_count == len(mock_from_records_rv)
