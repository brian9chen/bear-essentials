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
