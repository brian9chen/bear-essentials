from flask import current_app as app


class CartItem:
    def __init__(self, id, uid, inv_id, quantity, time_created, time_modified):
        self.id = id
        self.uid = uid
        self.inv_id = inv_id
        self.quantity = quantity
        self.time_created = time_created
        self.time_modified = time_modified

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, uid, inv_id, quantity, time_created, time_modified
        FROM CartItems
        WHERE id = :id
        ''',id=id)
        return CartItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
        SELECT c.id, c.uid, c.inv_id, c.quantity, c.time_created, c.time_modified, p.name, p.price
        FROM CartItems c, Inventory i, Products p
        WHERE c.uid = 0 AND c.inv_id = i.id AND i.pid = p.id
        ORDER BY time_created DESC
        ''',
                              uid=uid)
        return [{
            "cartitem_id": row[0],
            "uid": row[1],
            "inv_id": row[2],
            "quantity": row[3],
            "time_created": row[4],
            "time_modified": row[5],
            "product_name": row[6],
            "product_price": row[7]
        } for row in rows] if rows else []