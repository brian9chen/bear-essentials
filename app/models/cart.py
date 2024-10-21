from flask import current_app as app


class Cart:
    def __init__(self, id, user_id, total_price, time_created, time_modified):
        self.id = id
        self.name = name
        self.total_price = total_price
        self.time_created = time_created
        self.time_modified = time_modified

    @staticmethod
    def get(user_id):
        rows = app.db.execute('''
SELECT id, user_id, total_price
FROM Carts
WHERE user_id = :user_id
''',
                              id=id)
        return Carts(*(rows[0])) if rows is not None else None