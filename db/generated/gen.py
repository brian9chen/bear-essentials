from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import markovify
import pandas as pd

num_users = 100
num_products = 2000
num_purchases = 2500
num_reviews = 300
num_inventory = 4000
num_orders = 70
num_cart_items = 100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, quoting=csv.QUOTE_NONE, escapechar = '\\', dialect='unix')

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.street_address()
            balance = f'{str(fake.random_int(max=800))}.{fake.random_int(max=99):02}'
            is_seller = False
            writer.writerow([uid, email, password, firstname, lastname, address, balance, is_seller])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    categories = ['Fall', 'Winter', 'Spring', 'Summer'] 
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            creator_id = fake.random_int(min=1, max=(num_users-1))
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            category = fake.random_element(elements=categories)
            description = f"{category} inspired product: {fake.sentence(nb_words=8)}"
            discount_code = None
            prod_avg_rating = None
            image_path = None 
            available = fake.random_element(elements=('True', 'False'))
            if available == 'True':
                available_pids.append(pid)
            writer.writerow([pid, creator_id, name, price, description, category, discount_code, prod_avg_rating, image_path, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_reviews(num_reviews):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)

        userProductPairs = set()

        positiveReview = """
        I enjoyed this product and would recommend to others.
        Excellent quality and worth the price.
        Very happy with my purchase; it exceeded my expectations.
        """
        negativeReview = """
        This product did not match my expectations and I would not buy it again.
        The quality was disappointing for the price.
        Not satisfied with this purchase, and it doesn't work as advertised.
        """
        reviewModel = [positiveReview, negativeReview]

        for id in range(num_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)

            # make sure that a user can only leave 1 review an a product
            pair = str(uid) + "," + str(pid)
            while pair in userProductPairs:
                pid = fake.random_int(min=0, max=num_products-1)
                pair = str(uid) + "," + str(pid)
            userProductPairs.add(pair)

            # randomly choose if it is gonna be a postive or negative review
            sentiment = fake.random_int(min=0, max=1)

            # generate rating based on sentiment
            if sentiment == 0: # positive   
                rating = fake.random_int(min=3, max=5)
            else: # negative
                rating = fake.random_int(min=0, max=3)

            # generate review based on randomly chosen sentiment
            text_model = markovify.Text(reviewModel[sentiment])
            review = text_model.make_sentence()

            # randomly generate a time of creation
            time_posted = fake.date_time()
            time_modified = time_posted

            writer.writerow([id, uid, pid, rating, review, time_posted, time_modified, 0])
        print(f'{num_reviews} generated')
    return

def gen_inventory(num_inventory):
    products_df = pd.read_csv('Products.csv', names=['pid', 'creator_id', 'name', 'price', 'description', 'category', 'discount_code', 'image_path', 'available'])
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        
        for inventory_id in range(num_inventory):
            if inventory_id % 10 == 0:
                print(f'{inventory_id}', end=' ', flush=True)
            user_id = fake.random_int(min=0, max=num_users-1) 
            shop_name = f"{fake.word()} Shop"
            seller_avg_rating = f'{fake.random_int(min=30, max=50) / 10:.2f}'  
            pid = fake.random_int(min=0, max=num_products-1)  
            quantity_in_stock = fake.random_int(min=1, max=100)
            quantity_to_fulfill = fake.random_int(min=0, max=50)
            quantity_back_to_stock = fake.random_int(min=0, max=quantity_in_stock // 2)

            writer.writerow([inventory_id, user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock, shop_name, seller_avg_rating])
        
        print(f'{num_inventory} generated')
    return

def gen_orders(num_orders):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        order_ids = []
        for order_id in range(num_orders):
            if order_id % 10 == 0:
                print(f'{order_id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)  
            total_price = f'{fake.random_int(min=20, max=500)}.{fake.random_int(0, 99):02}' 
            time_created = fake.date_time_this_year()
            if fake.boolean(chance_of_getting_true=50): 
                time_fulfilled = fake.date_time_between_dates(datetime_start=time_created)
            else:
                time_fulfilled = None 
            writer.writerow([order_id, uid, total_price, time_created, time_fulfilled])
            order_ids.append(order_id) 
            
        print(f'{num_orders} generated')
    return order_ids

def gen_cart_items(num_cart_items, order_ids):
    with open('CartItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('CartItems...', end=' ', flush=True)
        
        for cart_id in range(num_cart_items):
            if cart_id % 10 == 0:
                print(f'{cart_id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)  
            inv_id = fake.random_int(min=0, max=num_inventory-1)  
            quantity = fake.random_int(min=1, max=10)  
            time_created = fake.date_time_this_year()
            time_modified = fake.date_time_between_dates(datetime_start=time_created)
            # if fake.boolean(chance_of_getting_true=30):  # 30% chance of being part of an order
            #     order_id = fake.random_element(elements=order_ids)
            #     time_fulfilled = fake.date_time_between_dates(datetime_start=time_created) if fake.boolean(chance_of_getting_true=70) else None
            # else:
            #     order_id = None
            #     time_fulfilled = None
            writer.writerow([cart_id, uid, inv_id, quantity, time_created, time_modified])
        
        print(f'{num_cart_items} generated')
    return

gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_reviews(num_reviews)
gen_inventory(num_inventory)
order_ids = gen_orders(num_orders)
gen_cart_items(num_cart_items, order_ids)