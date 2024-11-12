from flask import current_app as app


class Review:
    def __init__(self, id, user_id, product_id, rating, description, time_created, time_modified, num_upvotes):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.description = description
        self.time_created = time_created
        self.time_modified = time_modified
        self.num_upvotes = num_upvotes

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE id = :id
''',
                              id=id)
        return Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_by_uid(user_id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE user_id = :user_id
''',
                              user_id=user_id)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_5recent_reviews_by_uid(user_id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE user_id = :user_id
ORDER BY time_created DESC
LIMIT 5
''',
                              user_id=user_id)
        return [Review(*row) for row in rows]
    
    @staticmethod
    def get_reviews_by_seller_id(seller_id):
        rows = app.db.execute('''
        SELECT rating, description, time_created
        FROM Reviews
        WHERE seller_id = :seller_id
        ''', seller_id=seller_id)
        
        return [Review(*row) for row in rows]
