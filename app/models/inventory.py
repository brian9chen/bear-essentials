from flask import current_app as app
from flask import flash

class Inventory:
    def __init__(self, id, user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock, shop_name, seller_avg_rating):
        self.id = id
        self.user_id = user_id
        self.pid = pid
        self.quantity_in_stock = quantity_in_stock
        self.quantity_to_fulfill = quantity_to_fulfill
        self.quantity_back_to_stock = quantity_back_to_stock
        self.shop_name = shop_name
        self.seller_avg_rating = seller_avg_rating
    
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock
            FROM Inventory
            WHERE id = :id
        ''', id=id)
        return Inventory(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_user(user_id):
        user_id = int(user_id)  # Convert user_id to integer
        rows = app.db.execute('''
            SELECT i.id, i.user_id, i.pid, i.quantity_in_stock, i.quantity_to_fulfill, i.quantity_back_to_stock,
                p.name, p.price, p.description, p.category, p.image_path, p.creator_id
            FROM Inventory i
            JOIN Products p ON i.pid = p.id
            WHERE i.user_id = :user_id
        ''', user_id=user_id)

        inventory_items = []
        for row in rows:
            creator_id = int(row[11])  # convert creator_id to integer
            is_creator = (creator_id == user_id)

            inventory_items.append({
                "inventory_id": row[0],
                "user_id": row[1],
                "product_id": row[2],
                "quantity_in_stock": row[3],
                "quantity_to_fulfill": row[4],
                "quantity_back_to_stock": row[5],
                "product_name": row[6],
                "product_price": row[7],
                "product_description": row[8],
                "product_category": row[9],
                "image_path": row[10],
                "is_creator": is_creator
            })

        return inventory_items

    @staticmethod
    def add_product(user_id, product_name, quantity, price, category, description):
        # check if the product already exists in ur inventory
        existing_inventory = app.db.execute('''
            SELECT i.id 
            FROM Inventory i
            JOIN Products p ON i.pid = p.id
            WHERE i.user_id = :user_id AND p.name = :product_name AND p.category = :category
        ''', user_id=user_id, product_name=product_name, category=category)

        if existing_inventory:
            # flash message
            flash(f'Product "{product_name}" in category "{category}" already exists in your inventory. No changes made.', 'info')
            return

        # if the product already exists but not in your inventory
        existing_product = app.db.execute('''
            SELECT id FROM Products
            WHERE name = :product_name AND category = :category
        ''', product_name=product_name, category=category)

        app.db.execute('''
            UPDATE Users
            SET is_seller = True
            WHERE id = :user_id
        ''', user_id=user_id)

        if existing_product:
            # if the product exists in products, get the id
            product_id = existing_product[0][0]
        else:
            #create the product in the products table
            new_product = app.db.execute('''
                INSERT INTO Products (creator_id, name, price, category, description, available)
                VALUES (:user_id, :product_name, :price, :category, :description, TRUE)
                RETURNING id
            ''', user_id=user_id, product_name=product_name, price=price, category=category, description=description)
            product_id = new_product[0][0]

        #add the product to the users inventory
        app.db.execute('''
            INSERT INTO Inventory (user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock, shop_name, seller_avg_rating)
            VALUES (:user_id, :product_id, :quantity, 0, 0, :shop_name, 0)
        ''', user_id=user_id, product_id=product_id, quantity=quantity, shop_name="sample shop")


    @staticmethod
    def update_quantity(inventory_id, new_quantity):
        app.db.execute('''
            UPDATE Inventory
            SET quantity_in_stock = :new_quantity
            WHERE id = :inventory_id
        ''', new_quantity=new_quantity, inventory_id=inventory_id)

    @staticmethod
    def update_price(inventory_id, new_price):
        app.db.execute('''
            UPDATE Products
            SET price = :new_price
            FROM Inventory
            WHERE Products.id = Inventory.pid
            AND Inventory.id = :inventory_id
            AND Products.creator_id = Inventory.user_id
        ''', new_price=new_price, inventory_id=inventory_id)


    @staticmethod
    def remove_product(inventory_id):
        # delete an inventory item by id
        app.db.execute('''
            DELETE FROM Inventory
            WHERE id = :inventory_id
        ''', inventory_id=inventory_id)
    @staticmethod

    def update_description(inventory_id, new_description):
         app.db.execute('''
            UPDATE Products
            SET description = :new_description
            FROM Inventory
            WHERE Products.id = Inventory.pid
            AND Inventory.id = :inventory_id
            AND Products.creator_id = Inventory.user_id
    ''', new_description=new_description, inventory_id=inventory_id)
         
    @staticmethod
    def update_category(inventory_id, new_category):
        app.db.execute('''
            UPDATE Products
            SET category = :new_category
            FROM Inventory
            WHERE Products.id = Inventory.pid
            AND Inventory.id = :inventory_id
            AND Products.creator_id = Inventory.user_id
        ''', new_category=new_category, inventory_id=inventory_id)
    
    @staticmethod
    def update_name(inventory_id, new_name):
        app.db.execute('''
            UPDATE Products
            SET name = :new_name
            FROM Inventory
            WHERE Products.id = Inventory.pid
            AND Inventory.id = :inventory_id
            AND Products.creator_id = Inventory.user_id
        ''', new_name=new_name, inventory_id=inventory_id)
    
    # @staticmethod
    # def get_sellers_by_product(product_id):
    #     rows = app.db.execute('''
    #     SELECT u.firstname, u.lastname, i.shop_name, i.seller_avg_rating
    #     FROM Inventory i
    #     JOIN Users u ON i.user_id = u.id
    #     WHERE i.pid = :product_id
    # ''', product_id=product_id)
    #     return rows



    @staticmethod
    def update_image_path(inventory_id, image_path):
        """
        Update the image path for a specific inventory item.
        """
        # get product id from inventory id
        product = app.db.execute('''
        SELECT pid
        FROM Inventory
        WHERE id = :inventory_id
        ''', inventory_id=inventory_id)
        pid = product[0][0]

        # change product image path
        app.db.execute('''
        UPDATE Products
        SET image_path = :image_path
        WHERE id = :pid
        ''', pid=pid, image_path=image_path)

    @staticmethod
    def get_sales_data(user_id, year=None):
        query = '''
        SELECT p.name, EXTRACT(YEAR FROM o.time_created) as year, COALESCE(SUM(c.quantity), 0) as total_quantity_sold
        FROM Inventory i
        JOIN Products p ON i.pid = p.id
        LEFT JOIN CartItems c ON c.inv_id = i.id AND c.order_id IS NOT NULL
        LEFT JOIN Orders o ON c.order_id = o.id
        WHERE i.user_id = :user_id
        '''
        params = {'user_id': user_id}
        if year is not None:
            query += ' AND EXTRACT(YEAR FROM o.time_created) = :year'
            params['year'] = year

        query += '''
        GROUP BY p.name, year
        ORDER BY year DESC NULLS LAST, total_quantity_sold DESC
        '''
        rows = app.db.execute(query, **params)
        results = []
        products_in_results = set()

        # Process rows with sales data
        for row in rows:
            product_name = row[0]
            year_value = row[1]
            if year_value is not None:
                year_value = int(year_value)
            total_quantity_sold = int(row[2]) if row[2] is not None else 0

            results.append({
                'product_name': product_name,
                'year': year_value,
                'total_quantity_sold': total_quantity_sold
            })
            products_in_results.add(product_name)

        # Include products with no sales
        inv = app.db.execute('''
            SELECT *
            FROM Inventory
            WHERE user_id = :user_id
        ''', user_id=user_id)

        products_in_results = tuple(products_in_results)

        if inv:
            if products_in_results:
                # If there are products with sales, exclude them from the next query
                query_no_sales = '''
                SELECT p.name
                FROM Inventory i
                JOIN Products p ON i.pid = p.id
                WHERE i.user_id = :user_id AND p.name NOT IN :product_names
                '''
                params_no_sales = {'user_id': user_id, 'product_names': products_in_results}
            else:
                # No products had sales, so just select all products in inventory
                query_no_sales = '''
                SELECT p.name
                FROM Inventory i
                JOIN Products p ON i.pid = p.id
                WHERE i.user_id = :user_id
                '''
                params_no_sales = {'user_id': user_id}

            no_sales_rows = app.db.execute(query_no_sales, **params_no_sales)
            for row in no_sales_rows:
                product_name = row[0]
                if product_name not in products_in_results:
                    results.append({
                        'product_name': product_name,
                        'year': None,
                        'total_quantity_sold': 0
                    })

        return results


    @staticmethod
    def get_sales_years(user_id):
        rows = app.db.execute('''
        SELECT DISTINCT EXTRACT(YEAR FROM o.time_created) as year
        FROM Orders o
        JOIN CartItems c ON c.order_id = o.id
        JOIN Inventory i ON c.inv_id = i.id
        WHERE i.user_id = :user_id
        ORDER BY year DESC
        ''', user_id=user_id)
        years = [int(row[0]) for row in rows if row[0] is not None]
        return years


