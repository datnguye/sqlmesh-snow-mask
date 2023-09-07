from sqlmesh.core.macros import macro

from sqlmeshsm import macros

for item in macro.get_registry().items():
    print(item)
