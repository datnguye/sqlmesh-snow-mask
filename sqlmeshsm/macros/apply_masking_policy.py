from sqlmesh import macro


@macro()
def apply_masking_policy(
    evaluator,
    model: str,
    column: str,
    func: str,
    conditional_columns=[],
    materialization: str = "TABLE",
):
    return """
        ALTER {materialization} {model}
        modify column {column}
        set masking policy {func} using ({conditional_columns}) force;
        """.format(
        materialization=materialization,
        model=model,
        column=column,
        func=func,
        conditional_columns=",".join([x.name for x in conditional_columns.expressions]),
    )
