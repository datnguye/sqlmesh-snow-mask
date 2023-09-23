# sqlmeshsm [EXPERIMENTAL]

[![PyPI version](https://badge.fury.io/py/sqlmeshsm.svg)](https://pypi.org/project/sqlmeshsm/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.9|3.10|3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![codecov](https://codecov.io/gh/datnguye/sqlmesh-snow-mask/graph/badge.svg?token=ZcuyauQqoq)](https://codecov.io/gh/datnguye/sqlmesh-snow-mask)

[SQLMesh macros](https://sqlmesh.readthedocs.io/en/stable/concepts/macros/sqlmesh_macros/) used for ❄️ [Dynamic Masking Policies](https://docs.snowflake.com/en/user-guide/security-column-ddm-use) Implementation ✏️

**_Macro(s)_** 🚧 _(currently blocked by awaiting for more supports from the sqlmesh's  Macro Context)_

- `create_masking_policy` ([source](./sqlmeshsm/macros/create_masking_policy.py))
- `apply_masking_policy` ([source](./sqlmeshsm/macros/apply_masking_policy.py))

And, the Snowflake Hooker CLI (`hook`) ⭐

**_Hook(s)_** ✅

- `hook drop_masking_policy -c {config.yml} -mp {func}`

## Data Masking Development

### 1. Installation

```bash
pip install sqlmeshsm --upgrade
```

In your `(sqlmesh-project-dir)/macros/__init__.py`, let's import our lib:

```python
from sqlmeshsm import macros
```

### 2. Create masking policy functions

_For example_, the `customer` table needs the following masking policies:

- First Name: mask with `*` except the first 3 characters, fixed length of 10, no masking of `null`
- Last Name: mask with the first character of Full Name, no masking of `null`

There are 2 **masking functions**, they **must be created with following requirements**:

- 📂 Files located under `(your-sqlmesh-project)/macros/snow-mask-ddl`
- 🆎 File name format: `{mp_schema}.{mp_function_name}`

```sql
-- /snow-mask-ddl/mp_schema.mp_first_name.sql
CREATE MASKING POLICY IF NOT EXISTS @schema.mp_first_name AS (
    masked_column string
) RETURNS string ->
    LEFT(CASE
        WHEN masked_column IS NOT NULL THEN LEFT(masked_column, 3)
        ELSE NULL
    END || '**********', 10);
```

```sql
-- /snow-mask-ddl/mp_schema.mp_last_name.sql
CREATE MASKING POLICY IF NOT EXISTS @schema.mp_last_name AS (
    masked_column string,
    full_name_column string
) RETURNS string ->
    CASE
        WHEN masked_column IS NOT NULL THEN LEFT(full_name_column, 1)
        ELSE NULL
    END;
```

> `@schema` is the keyword to indicate the schema name which matches to the first part of the file name

## 3. Decide to mask model's columns

```sql
/* /models/my_customer_model.sql */
MODEL(
    name my_schema.my_customer_model
    kind FULL
    ...
)

/* MODEL SQL CODE HERE */

/* (optional) ADD this if `mp_schema` schema is not part of any models */
CREATE SCHEMA IF NOT EXISTS mp_schema;

/* REGISTER the masking functions */
@create_masking_policy(mp_schema.mp_first_name)
@create_masking_policy(mp_schema.mp_last_name)

/* APPLY the masking policies */
@apply_masking_policy(first_name, mp_schema.mp_first_name)
@apply_masking_policy(my_schema.my_customer_model, last_name, mp_schema.mp_last_name, ['full_name'])
```

Let's plan and apply it now: `sqlmesh plan --select-model my_schema.my_customer_model`

## 4. (Optional) Decide to clean up the masking policies

Let's run the built-in hooks:

```bash
hook drop_masking_policy \
    -c /path/to/sqlmesh/config.yml \
    -mp you_mp_function_name

# for example:
hook drop_masking_policy \
    -c ~\.sqlmesh\config.yml
    -mp common.mp_first_name
```

Here is the sample `config.yml` file, if you're not using sqlmesh but wanted to try the CLI:

```yml
# config.yml

gateways:
    masking_policy:
        connection:
            type: snowflake
            account: YOUR_VALUE
            user: YOUR_VALUE
            authenticator: externalbrowser
            # password: YOUR_VALUE
            warehouse: YOUR_VALUE
            database: YOUR_VALUE
            role: YOUR_VALUE
default_gateway: masking_policy
```

> Try `hook -h` for more options.

**_Voila! Happy Masking 🎉_**

## Contribution

[![buy me a coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?logo=buy-me-a-coffee&logoColor=white&labelColor=ff813f&style=for-the-badge)](https://www.buymeacoffee.com/datnguye)

If you've ever wanted to contribute to this tool, and a great cause, now is your chance!

See the contributing docs [CONTRIBUTING](./CONTRIBUTING.md) for more information.

Our **_Contributors_**:

<a href="https://github.com/datnguye/sqlmesh-snow-mask/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=datnguye/sqlmesh-snow-mask" />
</a>
