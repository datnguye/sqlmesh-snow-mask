import os

import snowflake.connector
import yaml
from pandas import DataFrame

from sqlmeshsm.hooks.helper import SQLQuery

sqlq = SQLQuery()


def drop_masking_policy(mp_func_name: str, config_path: str):
    """Drop masking policy by a given name

    Args:
        mp_func_name (str): Masking policy function
        config_path (str): Connection config file path
    """
    with open(config_path, "r") as yaml_file:
        config_content = yaml.safe_load(yaml_file)

    config = parse_sqlmesh_config(config=config_content)
    if not config:
        config = config_content

    # Engine initilization
    connection = snowflake.connector.connect(**config)
    cursor = connection.cursor()

    # Fetch & Unset masking policy references
    sql = sqlq.take("fetch_masking_policy_references")
    cursor.execute(command=sql, params=[mp_func_name])
    columns = DataFrame.from_records(
        iter(cursor), columns=[x[0] for x in cursor.description]
    )

    if not columns.empty:
        sql = sqlq.take("unset_masking_policy")
        for _, column in columns.iterrows():
            cursor.execute(
                command=sql.format(
                    column["MATERIALIZATION"], column["MODEL"], column["COLUMN_NAME"]
                ),
            )

    # Drop the masking policy
    cursor.execute(command=sqlq.take("drop_masking_policy").format(mp_func_name))

    # Clean up
    cursor.close()
    connection.close()


def parse_sqlmesh_config(config: dict):
    """Follow the SQLMesh config.yml file and parse the connection info

    Args:
        config (dict): Config.yml file content

    Returns:
        dict: Config dict or None if failed to parse
    """
    if not config:
        return None

    _config = (
        config.get("gateways", {})
        .get(config.get("default_gateway", ""), {})
        .get("connection")
    )
    if not _config:
        return None

    r = dict(
        user=_config.get("user"),
        password=_config.get("password"),
        account=_config.get("account"),
        warehouse=_config.get("warehouse"),
        database=_config.get("database"),
        session_parameters={
            "QUERY_TAG": f"sqlmeshsm-hook:{os.path.basename(__file__)}",
        },
    )

    if _config.get("authenticator"):
        r["authenticator"] = "externalbrowser"
        r.pop("password")

    return r
