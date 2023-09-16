from unittest import mock

import click
import pytest

from tests.unit.invocation import HookRunner


class TestRunner:
    @pytest.fixture
    def hook(self) -> HookRunner:
        return HookRunner()

    def test_runner_unhandled_exception(self, hook: HookRunner) -> None:
        with mock.patch(
            "sqlmeshsm.hooks.main.hook.make_context",
            side_effect=click.exceptions.Exit(-1),
        ):
            with pytest.raises(Exception):
                hook.invoke(["drop_masking_policy"])

    def test_group_invalid_option(self, hook: HookRunner) -> None:
        with pytest.raises(Exception):
            hook.invoke(["--invalid-option"])

    def test_command_invalid_option(self, hook: HookRunner) -> None:
        with pytest.raises(Exception):
            hook.invoke(["drop_masking_policy", "--invalid-option"])
        with pytest.raises(Exception):
            hook.invoke(["drop_masking_policy"])
        with pytest.raises(Exception):
            hook.invoke(["custom", "/path/to/noexisting.py"])

    @mock.patch("sqlmeshsm.hooks.main.drop_masking_policy")
    def test_command__drop_masking_policy(
        self, mock_drop_masking_policy, hook: HookRunner
    ) -> None:
        hook.invoke(
            [
                "drop_masking_policy",
                "--config",
                "/path/to/config.yml",
                "--masking-policy-function",
                "dummy",
            ]
        )
        mock_drop_masking_policy.assert_called_once_with(
            mp_func_name="dummy", config_path="/path/to/config.yml"
        )
