import importlib.metadata

import click

from sqlmeshsm.hooks.custom import run_custom_hook
from sqlmeshsm.hooks.drop_masking_policy import drop_masking_policy

__version__ = importlib.metadata.version("sqlmeshsm")

# hook
@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@click.version_option(__version__)
@click.pass_context
def hook(ctx, **kwargs):
    """Snowflake Hooker"""


# hook drop_masking_policy
@hook.command(name="drop_masking_policy")
@click.pass_context
@click.option(
    "--masking-policy-function",
    "-mp",
    help="Masking Policy function name",
    required=True,
    type=click.STRING,
)
@click.option(
    "--config",
    "-c",
    help="Connection config file path, or SQLMesh config path",
    required=True,
    type=click.STRING,
)
def hook__drop_masking_policy(ctx, **kwargs):
    """Snowflake Hook > Drop masking policy by given name [In Development]"""
    drop_masking_policy(
        mp_func_name=kwargs.get("masking_policy_function"),
        config_path=kwargs.get("config"),
    )


# hook custom /path/to/your_hook.py
@hook.command(name="custom")
@click.pass_context
@click.argument("filepath")
def hook__custom(ctx, filepath, **kwargs):
    """Custom Hook > Write your hook in python file and run"""
    run_custom_hook(path=filepath)
