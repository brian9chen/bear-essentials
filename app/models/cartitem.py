from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request


class CartItem:
    def __init__(self, id, uid, inv_id, quantity, time_created, time_modified):
        self.id = id
        self.uid = uid
        self.inv_id = inv_id
        self.quantity = quantity
        self.time_created = time_created
        self.time_modified = time_modified
        #self.order_id = order_id
        #self.time_fulfilled = time_fulfilled
        # self.is_fulfilled = is_fulfilled

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, uid, inv_id, quantity, time_created, time_modified
        FROM CartItems
        WHERE id = :id
        ''',id=id)
        return CartItem(*(rows[0])) if rows else None

    # this method only gets cart items that have NOT been submitted as orders yet (still in cart)
    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
        SELECT c.id, c.uid, c.inv_id, c.quantity, c.time_created, c.time_modified, p.name, p.price, u.id
        FROM CartItems c, Inventory i, Products p, Users u
        WHERE c.uid = :uid AND c.inv_id = i.id AND i.pid = p.id AND order_id IS NULL AND i.user_id = u.id
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
            "product_price": row[7],
            "seller_id": row[8]
        } for row in rows] if rows else []

    
    @staticmethod
    def mark_as_fulfilled(cartitem_id):
        """
        Mark a cart item as fulfilled.
        """
        app.db.execute('''
        UPDATE CartItems
        SET is_fulfilled = TRUE,
            time_fulfilled = CURRENT_TIMESTAMP,
            time_modified = CURRENT_TIMESTAMP
        WHERE id = :cartitem_id
        ''', cartitem_id=cartitem_id)

        # get the order_id associated with the cart item
        result = app.db.execute('''
        SELECT order_id
        FROM CartItems
        WHERE id = :cartitem_id
        ''', cartitem_id=cartitem_id)
        if result:
            order_id = result[0][0]

            # check if all cart items in the order are fulfilled
            unfulfilled_items = app.db.execute('''
            SELECT COUNT(*)
            FROM CartItems
            WHERE order_id = :order_id AND is_fulfilled = FALSE
            ''', order_id=order_id)
            unfulfilled_count = unfulfilled_items[0][0]

            if unfulfilled_count == 0:
                # all items are fulfilled; update the order's time_fulfilled
                app.db.execute('''
                UPDATE Orders
                SET time_fulfilled = CURRENT_TIMESTAMP
                WHERE id = :order_id
                ''', order_id=order_id)


#long code to get stuff by order
    @staticmethod
    def get_by_order(order_id, seller_id):
        """
        Get all cart items related to a specific order and seller.
        """
        rows = app.db.execute('''
        SELECT c.id, c.uid, c.inv_id, c.quantity, c.time_created, c.time_modified, c.order_id, c.is_fulfilled,
               p.name AS product_name, u.firstname || ' ' || u.lastname AS buyer_name, u.address AS buyer_address
        FROM CartItems c
        JOIN Inventory i ON c.inv_id = i.id
        JOIN Products p ON i.pid = p.id
        JOIN Users u ON c.uid = u.id
        WHERE c.order_id = :order_id AND i.user_id = :seller_id
        ORDER BY c.time_created DESC
        ''', order_id=order_id, seller_id=seller_id)
        return [{
            "cartitem_id": row[0],
            "buyer_id": row[1],
            "product_id": row[2],
            "quantity": row[3],
            "time_created": row[4],
            "time_modified": row[5],
            "order_id": row[6],
            "is_fulfilled": row[7],
            "product_name": row[8],
            "buyer_name": row[9],
            "buyer_address": row[10],
        } for row in rows]
    
    @staticmethod
    def add(pid, inv_uid, uid, quantity, seller_name):
        # get first and last name from seller name
        seller_names = seller_name.split()
        first_name = seller_names[0]
        last_name = seller_names[1]
        # gets user id from seller first and last name
        get_seller_id = app.db.execute(
            """
            SELECT u.id
            FROM Users u
            WHERE u.firstname = :first_name AND u.lastname = :last_name
            """,
            first_name=first_name,
            last_name=last_name
        )
        seller_id = get_seller_id[0][0]
        # gets inventory id from product id and inventory user id
        inv = app.db.execute(
            """
            SELECT i.id, i.quantity_in_stock
            FROM Inventory i
            WHERE i.pid = :pid AND i.user_id = :seller_id
            """,
            pid=pid,
            seller_id=seller_id
        )
        inv_id = inv[0][0]
        inv_quant = inv[0][1]
        if int(quantity) >= inv_quant:
            return False
        else:
            # uses attributes to make new cartitem
            rows = app.db.execute("""
            INSERT INTO CartItems(uid, inv_id, quantity)
            VALUES(:uid, :inv_id, :quantity)
            RETURNING id
            """,
                                uid=uid,
                                inv_id=inv_id,
                                quantity=quantity)
            id = rows[0][0]
            return True
        
    @staticmethod
    def get_items_by_order_id(order_id):
        rows = app.db.execute('''
        SELECT c.id, c.uid, c.inv_id, c.quantity, c.time_created, c.time_modified, p.name, p.price, c.is_fulfilled
        FROM CartItems c, Inventory i, Products p
        WHERE c.order_id = :order_id AND c.inv_id = i.id AND i.pid = p.id
        ORDER BY time_created DESC
        ''',
                              order_id=order_id)
        return [{
            "cartitem_id": row[0],
            "uid": row[1],
            "inv_id": row[2],
            "quantity": row[3],
            "time_created": row[4],
            "time_modified": row[5],
            "product_name": row[6],
            "product_price": row[7],
            "is_fulfilled": row[8]
        } for row in rows] if rows else []

    @staticmethod
    def delete(item_id):
        app.db.execute('''
        DELETE FROM CartItems
        WHERE id = :id
        ''', id=item_id)
    
    @staticmethod
    def change(item_id, new_quantity):
        app.db.execute('''
        UPDATE CartItems
        SET quantity = :quantity
        WHERE id = :id
        ''', id=item_id, quantity=new_quantity)
