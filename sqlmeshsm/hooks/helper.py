import os


class SQLQuery:
    def __init__(self) -> None:
        self.dir = f"{os.path.dirname(__file__)}/queries"

    def take(self, name: str) -> str:
        """Get SQL string from file

        Args:
            name (str): File name

        Returns:
            str: SQL content
        """
        try:
            with open(f"{self.dir}/{name}.sql", "r") as file:
                file_content = file.read()
        except Exception as e:
            return str(e)

        return file_content
