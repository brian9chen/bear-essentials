from flask import current_app as app

class Product:
    def __init__(self, id, creator_id, name, price, description, category, discount_code, image_path, available):
        self.id = id
        self.creator_id = creator_id
        self.name = name
        self.price = price
        self.description = description 
        self.category = category
        self.discount_code = discount_code
        # self.prod_avg_rating = prod_avg_rating
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
    @staticmethod
    def sort_and_filter(category, sort_order, keyword):
        query = '''
        SELECT *
        FROM Products
        WHERE 1 = 1
        '''

        # Add filtering by category 
        if category:
            query += ' AND category = :category'

        # Add filtering by keyword 
        if keyword:
            query += " AND (LOWER(name) LIKE LOWER(:keyword) OR LOWER(description) LIKE LOWER(:keyword))"

        # Add sorting based on sort_order
        if sort_order:
            if sort_order == 'price_asc':
                query += " ORDER BY price ASC"
            elif sort_order == 'price_desc':
                query += " ORDER BY price DESC"
            elif sort_order == 'name_asc':
                query += " ORDER BY name ASC"
            elif sort_order == 'name_desc':
                query += " ORDER BY name DESC"

        rows = app.db.execute(query, category=category, keyword=f"%{keyword}%" if keyword else None)
        return [Product(*row) for row in rows]

# MS2
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

    @staticmethod
    def get_sellers(product_id):
        rows = app.db.execute('''
            SELECT u.firstname, u.lastname, i.shop_name, i.seller_avg_rating
            FROM Inventory i
            JOIN Users u ON i.user_id = u.id
            WHERE i.pid = :product_id
        ''', product_id=product_id)
        
        unique_sellers = {}
        for seller in rows:
            firstname = seller[0]
            lastname = seller[1]
            shop_name = seller[2]
            seller_avg_rating = seller[3]
            
            key = (firstname, lastname, shop_name)
            if key not in unique_sellers:
                unique_sellers[key] = {
                    'firstname': firstname,
                    'lastname': lastname,
                    'shop_name': shop_name,
                    'seller_avg_rating': seller_avg_rating
                }
        
        return list(unique_sellers.values())

    @staticmethod
    def get_best_seller_ids():
        query = """
        SELECT p.id, COUNT(p.id)
        FROM Inventory i JOIN Products p ON i.pid = p.id LEFT JOIN CartItems c ON c.inv_id = i.id AND c.order_id IS NOT NULL 
            LEFT JOIN Orders o ON c.order_id = o.id 
        GROUP BY p.id
        ORDER BY COUNT(p.id) DESC;
        """
        try:
            rows = app.db.execute(query)
            # Extract and return only the product ids
            return [row[0] for row in rows]  
        except Exception as e:
            # Log the error for debugging
            print(f"Database error: {e}")
            return []
        
