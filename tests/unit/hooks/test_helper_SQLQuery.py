import pytest

from sqlmeshsm.hooks.helper import SQLQuery


class TestSQLQuery:
    @pytest.fixture
    def sqlquery(self) -> SQLQuery:
        return SQLQuery()

    def test_take__error(self, sqlquery):
        assert "No such file or directory" in sqlquery.take("")

    @pytest.mark.parametrize(
        "name, param",
        [
            ("drop_masking_policy", dict(dummy="dummy")),
            ("fetch_masking_policy_references", dict()),
            ("unset_masking_policy", dict()),
        ],
    )
    def test_take(self, name, param, sqlquery):
        with open(f"{sqlquery.dir}/{name}.sql", "r") as file:
            file_content = file.read()

        for key, value in param.items():
            file_content.replace(f"@{key}", value)

        assert file_content == sqlquery.take(name, **param)
