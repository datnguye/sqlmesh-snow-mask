from typing import List

import click

from sqlmeshsm.hooks.main import hook


class HookRunner:
    """Support runner for the programatic call"""

    def __init__(self) -> None:
        pass

    def invoke(self, args: List[str]):
        """Invoke a command of hook programatically

        Args:
            args (List[str]): hook arguments

        Raises:
            Exception: Unhandled exception
            Exception: Not Supported command exception
        """
        try:
            ctx = hook.make_context(hook.name, args)
            return hook.invoke(ctx)
        except click.exceptions.Exit as e:
            # 0 exit code, expected for --version early exit
            if str(e) == "0":
                return [], True
            raise Exception(f"unhandled exit code {str(e)}")
        except (click.NoSuchOption, click.UsageError) as e:
            raise Exception(e.message)
