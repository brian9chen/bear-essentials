from flask import current_app as app
from collections import namedtuple

ReviewWithProduct = namedtuple('ReviewWithProduct', ['review', 'product_name'])
ReviewWithSeller = namedtuple('ReviewWithProduct', ['review', 'seller_name'])


class Review:
    def __init__(self, id, user_id, product_id, seller_id, rating, description, time_created, time_modified, num_upvotes):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
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
    def count_product_reviews_by_uid(user_id):
        result = app.db.execute('''
SELECT COUNT(*) AS total_reviews
FROM Reviews r
WHERE r.user_id = :user_id AND r.product_id IS NOT NULL
''',
                        user_id=user_id)
        return int(result[0][0]) if result else 0
    
    @staticmethod
    def count_seller_reviews_by_uid(user_id):
        result = app.db.execute('''
SELECT COUNT(*) AS total_reviews
FROM Reviews r
WHERE r.user_id = :user_id AND r.seller_id IS NOT NULL
''',
                        user_id=user_id)
        return int(result[0][0]) if result else 0

    @staticmethod
    def get_all_prodName_by_uid(user_id, page=1, per_page=5):
        offset = (page - 1) * per_page
        rows = app.db.execute('''
SELECT r.*, p.name as product_name
FROM Reviews r
JOIN Products p ON r.product_id = p.id
WHERE r.user_id = :user_id AND r.product_id IS NOT NULL
ORDER BY r.time_created DESC
LIMIT :per_page OFFSET :offset
''',
                          user_id=user_id,
                          per_page=per_page,
                          offset=offset)
        return [ReviewWithProduct(Review(*row[:-1]), row[-1]) for row in rows]
    
    @staticmethod
    def get_all_sellerName_by_uid(user_id, page=1, per_page=5):
        offset = (page - 1) * per_page
        rows = app.db.execute('''
SELECT r.*, u.firstname || ' ' || u.lastname as seller_name
FROM Reviews r
JOIN Users u ON r.seller_id = u.id
WHERE r.user_id = :user_id AND r.seller_id IS NOT NULL
ORDER BY r.time_created DESC
LIMIT :per_page OFFSET :offset
''',
                          user_id=user_id,
                          per_page=per_page,
                          offset=offset)
        return [ReviewWithSeller(Review(*row[:-1]), row[-1]) for row in rows]
    
    @staticmethod
    def count_total_reviews():
        result = app.db.execute('''
SELECT COUNT(*) AS total_reviews
FROM Reviews
''')
        return int(result[0][0]) if result else 0
    
    @staticmethod
    def get_sortedByUpvote_by_pid(product_id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE product_id = :product_id
ORDER BY num_upvotes DESC
''',
                              product_id=int(product_id))
        return [Review(*row) for row in rows]

    @staticmethod
    def get_avg_rating_by_pid(product_id):
        result = app.db.execute('''
SELECT AVG(rating) AS avg_rating
FROM Reviews
WHERE product_id = :product_id
''',
                              product_id=int(product_id))
        return float(result[0][0]) if result and result[0][0] is not None else None
    
    @staticmethod
    def get_sortedByUpvote_by_sellerid(seller_id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE seller_id = :seller_id
ORDER BY num_upvotes DESC
''',
                              seller_id=int(seller_id))
        return [Review(*row) for row in rows]
    
    @staticmethod
    def get_avg_rating_by_pid(product_id):
        result = app.db.execute('''
SELECT AVG(rating) AS avg_rating
FROM Reviews
WHERE product_id = :product_id
''',
                              product_id=int(product_id))
        return float(result[0][0]) if result and result[0][0] is not None else None
    
    @staticmethod
    def get_avg_rating_by_sellerid(seller_id):
        result = app.db.execute('''
SELECT AVG(rating) AS avg_rating
FROM Reviews
WHERE seller_id = :seller_id
''',
                              seller_id=int(seller_id))
        return float(result[0][0]) if result and result[0][0] is not None else None
    
    @staticmethod
    def get_by_id(id):
        rows = app.db.execute('''
SELECT id, user_id, product_id, seller_id, rating, description, time_created, time_modified, num_upvotes
FROM Reviews
WHERE id = :id
        ''',
                                id=id)
        return Review(*rows[0]) if rows else None
    
    @staticmethod
    def has_user_reviewed_product(user_id, product_id):
        rows = app.db.execute('''
SELECT id FROM Reviews 
WHERE user_id = :user_id AND product_id = :product_id
        ''', 
                                user_id=user_id, product_id=product_id)
        return rows[0] if rows else None
    
    @staticmethod
    def has_user_reviewed_seller(user_id, seller_id):
        rows = app.db.execute('''
SELECT id FROM Reviews 
WHERE user_id = :user_id AND seller_id = :seller_id
        ''', 
                                user_id=user_id, seller_id=seller_id)
        return rows[0] if rows else None
    
    @staticmethod
    def change_upvote_count(review_id, change):
        app.db.execute('''
UPDATE Reviews
SET num_upvotes = num_upvotes + :change
WHERE id = :review_id
        ''',
                                change=change, review_id=review_id)
        
        
    @staticmethod
    def get_user_vote(user_id, review_id):
        rows = app.db.execute('''
        SELECT vote_type
        FROM ReviewVotes
        WHERE user_id = :user_id AND review_id = :review_id
        ''',
        user_id=user_id,
        review_id=review_id)
        return rows[0][0] if rows else None

    @staticmethod
    def change_upvote_count(review_id, user_id, is_upvote):
        # Check if user has already voted
        current_vote = Review.get_user_vote(user_id, review_id)
        
        if current_vote is None:
            # First time voting
            vote_type = 1 if is_upvote else -1
            app.db.execute('''
            INSERT INTO ReviewVotes (user_id, review_id, vote_type)
            VALUES (:user_id, :review_id, :vote_type)
            ''',
            user_id=user_id,
            review_id=review_id,
            vote_type=vote_type)
            
            # Update review count
            app.db.execute('''
            UPDATE Reviews
            SET num_upvotes = num_upvotes + :change
            WHERE id = :review_id
            ''',
            change=vote_type,
            review_id=review_id)
            
            return True
            
        elif (is_upvote and current_vote == -1) or (not is_upvote and current_vote == 1):
            # Changing vote from down to up or up to down
            new_vote_type = 1 if is_upvote else -1
            app.db.execute('''
            UPDATE ReviewVotes
            SET vote_type = :new_vote_type
            WHERE user_id = :user_id AND review_id = :review_id
            ''',
            new_vote_type=new_vote_type,
            user_id=user_id,
            review_id=review_id)
            
            # Update review count (multiply by 2 because we're changing from -1 to 1 or vice versa)
            app.db.execute('''
            UPDATE Reviews
            SET num_upvotes = num_upvotes + :change
            WHERE id = :review_id
            ''',
            change=new_vote_type * 2,
            review_id=review_id)
            
            return True
            
        return False  # User has already voted this way
    
#     @staticmethod
#     def get_reviews_by_seller_id(seller_id):
#         rows = app.db.execute('''
# SELECT rating, description, time_created
# FROM Reviews
# WHERE seller_id = :seller_id
# ''',
#                             seller_id=seller_id)
#         return [Review(*row) for row in rows]
