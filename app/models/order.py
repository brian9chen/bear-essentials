from flask import current_app as app

class Order:
    def __init__(self, id, uid, total_price, time_created, time_fulfilled):
        self.id = id
        self.uid = uid
        self.total_price = total_price
        self.time_created = time_created
        self.time_fulfilled = time_fulfilled

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, uid, total_price, time_created, time_fulfilled
        FROM Orders
        WHERE id = :id
        ''',id=id)
        return Order(*(rows[0])) if rows else None

    @staticmethod
    def submit(uid, total_price):
        rows = app.db.execute("""
        INSERT INTO Orders(uid, total_price)
        VALUES(:uid, :total_price)
        RETURNING id
        """,
                              uid=uid,
                              total_price=total_price)
        id = rows[0][0]
        return Order.get(id)
    
    @staticmethod
    def get_all_by_seller(seller_id):
            rows = app.db.execute('''
                SELECT DISTINCT o.id, o.uid, o.total_price, o.time_created, o.time_fulfilled
                FROM Orders o
                JOIN CartItems c ON o.id = c.order_id
                JOIN Inventory i ON c.inv_id = i.id
                WHERE i.user_id = :seller_id
                ORDER BY o.time_created DESC
            ''', seller_id=seller_id)
            return [Order(*row) for row in rows] if rows else []