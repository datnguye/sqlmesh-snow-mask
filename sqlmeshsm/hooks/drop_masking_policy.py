import pandas as pd
import snowflake.connector
import yaml


def drop_masking_policy(mp_func_name: str, config_path: str):
    """Drop masking policy by a given name

    Args:
        mp_func_name (str): Masking policy function
        config_path (str): Connection config file path
    """
    with open(config_path, "r") as yaml_file:
        config_content = yaml.safe_load(yaml_file)

    config = __parse_sqlmesh_config(config=config_content)
    if not config:
        config = config_content

    # Engine initilization
    connection = snowflake.connector.connect(**config)
    cursor = connection.cursor()

    # Fetch & Unset masking policy references
    cursor.execute(
        f"""
        SELECT  C.COLUMN_NAME as COLUMN,
                T.TABLE_CATALOG || '.' || T.TABLE_SCHEMA || '.' || T.TABLE_NAME AS MODEL,
                T.TABLE_TYPE as MATERIALIZATION
                
        FROM    INFORMATION_SCHEMA.MASKING_POLICY_REFERENCES AS M
        JOIN    INFORMATION_SCHEMA.COLUMNS AS C
            ON  M.REF_COLUMN_NAME = C.COLUMN_NAME
            AND M.REF_TABLE_NAME = C.TABLE_NAME
            AND M.REF_TABLE_SCHEMA = C.TABLE_SCHEMA
        JOIN    INFORMATION_SCHEMA.TABLES AS T
            ON  M.TABLE_NAME = T.TABLE_NAME
            AND M.TABLE_SCHEMA = T.TABLE_SCHEMA
        
        WHERE   M.MASKING_POLICY_FUNCTION_NAME = '{mp_func_name}';
    """
    )
    columns = pd.DataFrame.from_records(
        iter(cursor), columns=[x[0] for x in cursor.description]
    )

    for column in columns:
        cursor.execute(
            expressions=f"""
            ALTER TABLE {column.materialization} {column.model}
            ALTER COLUMN {column.column}
            UNSET MASKING POLICY;
        """
        )

    # Drop the masking policy
    cursor.execute(expressions=f"DROP MASKING POLICY {mp_func_name};")

    # Clean up
    cursor.close()
    connection.close()


def __parse_sqlmesh_config(config: dict):
    """Follow the SQLMesh config.yml file and parse the connection info

    Args:
        config (dict): Config.yml file content

    Returns:
        dict: Config dict or None if failed to parse
    """
    return (
        config.get("gateways", {})
        .get(config.get("default_gateway", ""), {})
        .get("connection")
    )
