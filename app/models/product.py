from flask import current_app as app
# need to fix SQL injection attacks 

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

# GET METHODS  
# get product based on id 
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None
    
# get all available products 
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

# get all categories 
    @staticmethod
    def get_categories():
        rows = app.db.execute('''
SELECT DISTINCT category
FROM Products
WHERE category IS NOT NULL
''')
        return [row[0] for row in rows]

# FILTER & SORT METHODS 
# filter by category 
    @staticmethod
    def filter_by_category(category):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE category = :category
''',
                              category=category)
        return [Product(*row) for row in rows]

# filter by keywords in name / description 
    @staticmethod
    def filter_by_keyword(keyword):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE LOWER(name) LIKE LOWER(:keyword)
    OR LOWER(description) LIKE LOWER(:keyword)
''',
                              keyword = f"%{keyword}%")
        return [Product(*row) for row in rows]

# sort by price asc
    @staticmethod
    def sort_by_price_asc():
        rows = app.db.execute('''
SELECT *
FROM Products
ORDER BY price ASC
''')
        return [Product(*row) for row in rows]

# sort by price desc
    @staticmethod
    def sort_by_price_desc():
        rows = app.db.execute('''
SELECT *
FROM Products
ORDER BY price DESC
''')
        return [Product(*row) for row in rows]

# rework this?
# sort by rating 
    @staticmethod 
    def sort_by_prod_rating():
        rows = app.db.execute('''
SELECT *
FROM Products
ORDER BY prod_avg_rating
''')
        return [Product(*row) for row in rows]

# get most expensive k products 
    @staticmethod 
    def most_expensive_products(k):
        rows = app.db.execute('''
SELECT *
FROM Products
ORDER BY price DESC
LIMIT :k
''', k=k)
        return [Product(*row) for row in rows]

# comment 
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
    @staticmethod
    def get_unique_categories():
        rows = app.db.execute('''
            SELECT DISTINCT category
            FROM Products
        ''')
        return [row[0] for row in rows]

    
