from SQLeasy import cursor_


class Database:
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def all(cls):
        cursor_.execute("SHOW DATABASES")
        return [Database(i[0]) for i in cursor_.fetchall()]

    def create(self):
        cursor_.execute(f"CREATE DATABASE IF NOT EXISTS {self.name}")

    def drop(self):
        cursor_.execute(f"DROP DATABASE {self.name}")

    @property
    def tables(self):
        cursor_.execute(f"USE {self.name}")
        cursor_.execute("SHOW TABLES")
        return [Table(i[0], self) for i in cursor_.fetchall()]


class Table:
    def __init__(self, name: str, database: Database, cols: list = None):
        self.name = name
        self.database = database
        self.cols = cols

    def create(self):
        cursor_.execute(
            f"CREATE TABLE IF NOT EXISTS {self.database.name}.{self.name} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join(self.cols)})"
        )

    def drop(self):
        cursor_.execute(f"DROP TABLE {self.database.name}.{self.name}")

    @property
    def description(self):
        cursor_.execute(f"USE {self.database.name}")
        cursor_.execute(f"DESCRIBE {self.name}")
        return cursor_.fetchall()

    @property
    def create_stmt(self):
        cursor_.execute(f"USE {self.database.name}")
        cursor_.execute(f"SHOW CREATE TABLE {self.name}")
        return cursor_.fetchall()
