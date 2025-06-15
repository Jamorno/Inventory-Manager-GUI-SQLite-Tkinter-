import sqlite3

class InventoryDB:
    def __init__(self, db_name="inventory_db.sqlite3") -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS inventory (product_name TEXT PRIMARY KEY, quantity INTEGER)"""
        )
        self.conn.commit()

    def add_item(self, product_name, quantity=1):
        self.cursor.execute("SELECT quantity FROM inventory WHERE product_name=?", (product_name,))
        result = self.cursor.fetchone()

        if result:
            new_quantity = result[0] + quantity
            self.cursor.execute("UPDATE inventory SET quantity=? WHERE product_name=?", (new_quantity, product_name))
        else:
            self.cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (?, ?)", (product_name, quantity))

        self.conn.commit()

    def remove_item(self, product_name, quantity=1):
        self.cursor.execute("SELECT quantity FROM inventory WHERE product_name=?", (product_name,))
        result = self.cursor.fetchone()

        if result:
            new_quantity = result[0] - quantity
            if new_quantity <= 0:
                self.cursor.execute("DELETE FROM inventory WHERE product_name=?", (product_name,))
            else:
                self.cursor.execute("UPDATE inventory SET quantity=? WHERE product_name=?", (new_quantity, product_name))
            self.conn.commit()

    def show_stock(self):
        self.cursor.execute("SELECT product_name, quantity FROM inventory")
        rows = self.cursor.fetchall()

        if not rows:
            return "No product in stock."
        return "\n".join(f"{name}: {qty}" for name, qty in rows)
