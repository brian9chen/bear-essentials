from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased, quantity, price):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.quantity = quantity
        self.price = price

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_id(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]
    

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased, quantity, price
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''', 
                              uid=uid)
        return [Purchase(*row) for row in rows]

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'pid': self.pid,
            'time_purchased': self.time_purchased.isoformat(),
            'quantity': self.quantity,
            'price': self.price
        }
