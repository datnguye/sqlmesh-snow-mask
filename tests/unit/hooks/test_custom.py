import os

import pytest

from sqlmeshsm.hooks.custom import run_custom_hook


class TestCustom:
    # @pytest.mark.parametrize(
    #     "path",
    #     [
    #         ("")
    #     ]
    # )
    def test_run_custom_hook_failed(self):
        with pytest.raises(Exception):
            run_custom_hook(path="/file_not_found.py")

    def test_run_custom_hook_good(self, capsys):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        run_custom_hook(path=f"{dir_path}/hello.py")
        captured = capsys.readouterr()
        assert captured.out == "hello world\n"
