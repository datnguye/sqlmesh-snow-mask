import pytest

from sqlmeshsm.hooks.helper import SQLQuery


class TestSQLQuery:
    @pytest.fixture
    def sqlquery(self) -> SQLQuery:
        return SQLQuery()

    def test_take__error(self, sqlquery):
        assert "No such file or directory" in sqlquery.take("")

    @pytest.mark.parametrize(
        "name",
        [
            ("drop_masking_policy"),
            ("fetch_masking_policy_references"),
            ("unset_masking_policy"),
        ],
    )
    def test_take(self, name, sqlquery):
        with open(f"{sqlquery.dir}/{name}.sql", "r") as file:
            file_content = file.read()

        assert file_content == sqlquery.take(name)
