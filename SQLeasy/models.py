from SQLeasy import cursor_


class Database:
    def __init__(self, name: str):
        self.name = name

    def show_tables(self):
        cursor_.execute(f"USE {self.name}")
        cursor_.execute("SHOW TABLES")
        return [Table(i[0], self) for i in cursor_.fetchall()]


class Table:
    def __init__(self, name: str, database: Database):
        self.name = name
        self.database = database

    def describe(self):
        cursor_.execute(f"USE {self.database.name}")
        cursor_.execute(f"DESCRIBE {self.name}")
        return cursor_.fetchall()

    def show_create(self):
        cursor_.execute(f"USE {self.database.name}")
        cursor_.execute(f"SHOW CREATE TABLE {self.name}")
        return cursor_.fetchall()
