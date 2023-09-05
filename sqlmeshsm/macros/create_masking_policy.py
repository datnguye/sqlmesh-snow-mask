import os

from sqlmesh import macro


@macro()
def create_masking_policy(
    evaluator, func: str, ddl_dir: str = f"{os.getcwd()}/macros/snow-mask-ddl"
):
    ddl_file = f"{ddl_dir}/{func}.sql"
    func_parts = str(func).split(".")
    if len(func_parts) != 2:
        raise Exception("Function name must be 2 parts e.g. `schema.mp_name.sql`")

    schema = func_parts[0]
    with open(ddl_file, "r") as file:
        content = file.read()

    return ";".join(
        [f"CREATE SCHEMA IF NOT EXISTS {schema}", content.replace("@schema", schema)]
    )
