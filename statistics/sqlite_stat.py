import sqlite3


from statistics.statistics_base import StatisticsBase


class SQLiteHandler(StatisticsBase):
    def __init__(self, db_name = "stats.db"):
        self.conn = sqlite3.connect(db_name)

        self.__create_tables()

    def __create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id str PRIMARY KEY,
                figi str,
                direction TEXT,
                price REAL,
                quantity INTEGER,
                status TEXT
            )
            """
        )
    
    async def get_orders(self):
        return self.execute_select("SELECT * FROM orders")

    async def add_order(self, order_id, figi, order_direction, price, quantity, status):
        self.execute_insert(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, figi, order_direction, price, quantity, status),
        )


    async def update_order_status(self, order_id, status):
        self.execute_update(
            "UPDATE orders SET status=? WHERE id=?",
            (status, order_id),
        )

    def close(self):
        self.conn.close()

    def execute(self, sql, params=None):
        if params is None:
            params = []
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.fetchall()

    def execute_insert(self, sql, params=None):
        if params is None:
            params = []
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.lastrowid

    def execute_update(self, sql, params=None):
        if params is None:
            params = []
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.rowcount

    def execute_delete(self, sql, params=None):
        if params is None:
            params = []
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.rowcount

    def execute_select(self, sql, params=None):
        if params is None:
            params = []
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def execute_select_one(self, sql, params=None):
        if params is None:
            params = []
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()
