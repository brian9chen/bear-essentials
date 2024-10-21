from flask import current_app as app


class Inventory:
    def __init__(self, id, user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock):
        self.id = id
        self.user_id = user_id
        self.pid = pid
        self.quantity_in_stock = quantity_in_stock
        self.quantity_to_fulfill = quantity_to_fulfill
        self.quantity_back_to_stock = quantity_back_to_stock

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock
            FROM Inventory
            WHERE id = :id
        ''',id=id)
        return Inventory(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_user(user_id):
        rows = app.db.execute('''
            SELECT i.id, i.user_id, i.pid, i.quantity_in_stock, i.quantity_to_fulfill, i.quantity_back_to_stock,
                   p.name, p.price, p.description, p.category
            FROM Inventory i
            JOIN Products p ON i.pid = p.id
            WHERE i.user_id = :user_id
        ''', user_id=user_id)

        return [{
            "inventory_id": row[0],
            "user_id": row[1],
            "product_id": row[2],
            "quantity_in_stock": row[3],
            "quantity_to_fulfill": row[4],
            "quantity_back_to_stock": row[5],
            "product_name": row[6],
            "product_price": row[7],
            "product_description": row[8],
            "product_category": row[9]
        } for row in rows] if rows else []