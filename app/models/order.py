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