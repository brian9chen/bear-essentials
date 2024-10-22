from flask import current_app as app
from .purchase import Purchase


class Product:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def getPurchasesProducts(user_id):
        rows = app.db.execute('''
SELECT p.id AS purchase_id, pr.id AS product_id, pr.name AS product_name, 
       pr.price, p.time_purchased
FROM Purchases p
JOIN Products pr ON p.pid = pr.id
WHERE p.uid = :user_id
ORDER BY p.time_purchased DESC
''',
                              user_id=user_id)
        
        return [
            {
                'purchase_id': row[0],
                'product_id': row[1],
                'product_name': row[2],
                'price': row[3],
                'time_purchased': row[4]
            }
            for row in rows
        ]
