from flask import current_app as app
from .cartitem import CartItem

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
    def submit(uid):
        # checking if the order can go through
        b = app.db.execute('''
        SELECT balance
        FROM users
        WHERE id = :uid
        ''', uid=uid)
        user_balance = int(b[0][0])

        # loop through to check item quantity, available quantity, and price
        cart_items = CartItem.get_all_by_uid(uid)
        total = 0
        for item in cart_items:
            total += item['product_price']
            quant = app.db.execute('''
            SELECT quantity_in_stock
            FROM Inventory
            WHERE id = :inv_id
            ''', inv_id=item['inv_id'])
            avail = quant[0][0]
            if item['quantity'] > avail:
                return True
        if total > user_balance:
            return False

        # making new order
        rows = app.db.execute("""
        INSERT INTO Orders(uid)
        VALUES(:uid)
        RETURNING id
        """, uid=uid)
        order_id = rows[0][0]

        # loop through each cart item - assign it to the new order, decrement user balance, increment seller balance, decrement qty in stock
        total_price = 0
        for item in cart_items:
            # assign to the new order
            app.db.execute('''
            UPDATE CartItems
            SET order_id = :order_id
            WHERE id = :id
            ''', id=item['cartitem_id'], order_id=order_id)
            
            # calculate total price
            total_price += item['quantity'] * item['product_price']

            # decrement user balance
            app.db.execute('''
            UPDATE Users
            SET balance = balance - :cur_price
            WHERE id = :uid
            ''', cur_price=item['quantity'] * item['product_price'], uid=uid)

            # increment seller balance
            app.db.execute('''
            UPDATE Users
            SET balance = balance + :cur_price
            WHERE id = :uid
            ''', cur_price=item['quantity'] * item['product_price'], uid=item['seller_id'])

            # decrement inv quantity in stock
            app.db.execute('''
            UPDATE Inventory
            SET quantity_in_stock = quantity_in_stock - :quantity
            WHERE id = :id
            ''', id=item['inv_id'], quantity=item['quantity'])

        # update new order with total price
        app.db.execute('''
        UPDATE Orders
        SET total_price = :total_price
        WHERE id = :id
        ''', id=order_id, total_price=total_price)

        return order_id
    
    @staticmethod
    def get_seller_orders_with_items(seller_id, search=None, status_filter="all"):
        # search clause to filter orders by product name or buyer name
        search_clause = ''
        if search:
            search_clause = '''
            AND (
                LOWER(p.name) LIKE LOWER(:search)
                OR LOWER(u.firstname || ' ' || u.lastname) LIKE LOWER(:search)
            )
            '''

        # status filter clause
        status_clause = ''
        if status_filter == "pending":
            status_clause = 'AND of.overall_fulfilled = 0'
        elif status_filter == "fulfilled":
            status_clause = 'AND of.overall_fulfilled = 1'

        # main query
        query = f'''
        WITH order_fulfillment AS (
            SELECT o.id AS order_id,
                MIN(c.is_fulfilled::int) AS overall_fulfilled
            FROM Orders o
            JOIN CartItems c ON o.id = c.order_id
            JOIN Inventory i ON c.inv_id = i.id
            WHERE i.user_id = :seller_id
            GROUP BY o.id
        )
        SELECT o.id AS order_id, o.uid AS buyer_id, SUM(c.quantity * p.price) AS seller_total_price,
            COUNT(c.id) AS total_items, o.time_created, o.time_fulfilled,
            c.id AS cartitem_id, c.quantity, c.is_fulfilled,
            p.name AS product_name, u.firstname || ' ' || u.lastname AS buyer_name,
            u.address AS buyer_address, of.overall_fulfilled
        FROM Orders o
        JOIN CartItems c ON o.id = c.order_id
        JOIN Inventory i ON c.inv_id = i.id
        JOIN Products p ON i.pid = p.id
        JOIN Users u ON o.uid = u.id
        JOIN order_fulfillment of ON o.id = of.order_id
        WHERE i.user_id = :seller_id
        {search_clause}
        {status_clause}
        GROUP BY o.id, o.uid, o.time_created, o.time_fulfilled,
                c.id, c.quantity, c.is_fulfilled,
                p.name, u.firstname, u.lastname, u.address, of.overall_fulfilled
        ORDER BY o.time_created DESC
        '''
        rows = app.db.execute(query, seller_id=seller_id, search=f"%{search}%" if search else None)

        orders = {}
        for row in rows:
            order_id = row[0]
            if order_id not in orders:
                orders[order_id] = {
                    "order_id": row[0],
                    "buyer_id": row[1],
                    "seller_total_price": row[2],
                    "total_items": row[3],
                    "time_created": row[4],
                    "time_fulfilled": row[5],
                    "items": [],
                    "overall_fulfilled": bool(row[12]) 
                }
            orders[order_id]["items"].append({
                "cartitem_id": row[6],
                "quantity": row[7],
                "is_fulfilled": row[8],
                "product_name": row[9],
                "buyer_name": row[10],
                "buyer_address": row[11],
            })
        return list(orders.values())
    
    @staticmethod
    def get_orders_by_user(uid):
        rows = app.db.execute('''
        SELECT id, total_price, time_created, time_fulfilled
        FROM Orders
        WHERE uid = :uid
        ''', uid=uid)
        return [{
            "id": row[0],
            "total_price": row[1],
            "time_created": row[2],
            "time_fulfilled": row[3]
        } for row in rows] if rows else []
