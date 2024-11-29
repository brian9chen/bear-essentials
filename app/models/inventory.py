from flask import current_app as app

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
        rows = app.db.execute('''
            SELECT i.id, i.user_id, i.pid, i.quantity_in_stock, i.quantity_to_fulfill, i.quantity_back_to_stock,
                p.name, p.price, p.description, p.category, i.image_path
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
        "product_category": row[9],
        "image_path": row[10]  # Add this line
    } for row in rows] if rows else []


    @staticmethod
    def add_product(user_id, product_name, quantity, price, category, description):
        product_id = app.db.execute('''
            INSERT INTO Products (creator_id, name, price, category, description)
            VALUES (:user_id, :product_name, :price, :category, :description)
            RETURNING id
        ''', user_id=user_id, product_name=product_name, price=price, category=category, description = description)
        
        # insert the new product into the Inventory table with initial quantity
        if product_id:
            app.db.execute('''
                INSERT INTO Inventory (user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock, shop_name, seller_avg_rating)
                VALUES (:user_id, :product_id, :quantity, 0, 0, :name, 0)
            ''', user_id=user_id, product_id=product_id[0][0], quantity=quantity, name="sample name")

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



    @staticmethod
    def update_image_path(inventory_id, image_path):
        """
        Update the image path for a specific inventory item.
        """
        app.db.execute('''
        UPDATE Inventory
        SET image_path = :image_path
        WHERE id = :inventory_id
        ''', inventory_id=inventory_id, image_path=image_path)


