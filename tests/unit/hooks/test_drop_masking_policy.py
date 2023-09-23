from unittest import mock

import pytest
from pandas import DataFrame

from sqlmeshsm.hooks import drop_masking_policy


class TestDropMaskingPolicy:
    @pytest.mark.parametrize(
        "config, result",
        [
            (
                dict(
                    gateways=dict(
                        data=dict(
                            connection=dict(
                                user="data",
                                password="data",
                                account="data",
                                warehouse="data",
                                database="data",
                            )
                        )
                    ),
                    default_gateway="data",
                ),
                dict(
                    user="data",
                    password="data",
                    account="data",
                    warehouse="data",
                    database="data",
                    session_parameters=dict(
                        QUERY_TAG="sqlmeshsm-hook:drop_masking_policy.py"
                    ),
                ),
            ),
            (
                dict(
                    gateways=dict(
                        data=dict(
                            connection=dict(
                                user="data",
                                authenticator="externalbrowser",
                                account="data",
                                warehouse="data",
                                database="data",
                            )
                        )
                    ),
                    default_gateway="data",
                ),
                dict(
                    user="data",
                    account="data",
                    warehouse="data",
                    database="data",
                    session_parameters=dict(
                        QUERY_TAG="sqlmeshsm-hook:drop_masking_policy.py"
                    ),
                    authenticator="externalbrowser",
                ),
            ),
            (None, None),
        ],
    )
    def test_parse_sqlmesh_config(self, config, result):
        assert result == drop_masking_policy.parse_sqlmesh_config(config=config)

    @pytest.mark.parametrize(
        "mock_from_records_rv",
        [
            (DataFrame()),
            (
                DataFrame(
                    [("my_column", "my_model", "table")],
                    columns=["COLUMN_NAME", "MODEL", "MATERIALIZATION"],
                )
            ),
        ],
    )
    @mock.patch("sqlmeshsm.hooks.drop_masking_policy.DataFrame.from_records")
    @mock.patch("snowflake.connector.connect")
    @mock.patch("sqlmeshsm.hooks.helper.SQLQuery.take")
    @mock.patch(
        "builtins.open",
        mock.mock_open(
            read_data="""
                user: data
                password: data
                account: data
                warehouse: data
                database: data
            """
        ),
    )
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
            mock.call("fetch_masking_policy_references"),
            mock.call("drop_masking_policy"),
        ]
        mock_SQLQuery_take.assert_has_calls(
            calls, any_order=(len(mock_from_records_rv) != 0)
        )
        mock_connector_connect.assert_called_once()
        if not mock_from_records_rv.empty:
            assert mock_from_records.call_count == len(mock_from_records_rv)
