from flask import current_app as app


class Product:
    def __init__(self, id, creator_id, name, price, description, category, discount_code, prod_avg_rating, image_path, available):
        self.id = id
        self.creator_id = creator_id
        self.name = name
        self.price = price
        self.description = description 
        self.category = category
        self.discount_code = discount_code 
        self.prod_avg_rating = prod_avg_rating
        self.image_path = image_path
        self.available = available 

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
    @staticmethod 
    def most_expensive_products(k):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        ORDER BY price DESC
        LIMIT :k
        ''', k=k)
        return [Product(*row) for row in rows]
    
