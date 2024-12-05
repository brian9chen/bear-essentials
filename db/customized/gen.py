from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import markovify
import pandas as pd

num_users = 100
num_products = 100
num_sellers = 50
num_purchases = 2500
num_reviews = 300
num_inventory = 4000
num_orders = 70
num_cart_items = 100
num_coupons = 10
available_pids = list(range(100))


Faker.seed(0)
fake = Faker()
random.seed(0)

temp_user_ids = [uid for uid in range(num_users) if uid != 1]
seller_ids = random.sample(temp_user_ids, num_sellers)
#seller_ids = random.sample(range(2, num_users), num_sellers)



def get_csv_writer(f):
    return csv.writer(f, quoting=csv.QUOTE_NONE, escapechar = '\\', dialect='unix')

def gen_users(num_users, seller_ids):
    with open('Users.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        
        writer.writerow([0, 'icecream@tastes.good', 'pbkdf2:sha256:260000$1GvmeoAkcWb89TyU$5f711eafb243c1c1a884715dd9bd6d185f29ccd3dab59ad19cc201a7260091cb', 'Joey', 'Shmoey', '123 Ice Cream Lane', 0, True])
        writer.writerow([1, 'coolbeans@coffee.strong', 'pbkdf2:sha256:260000$1GvmeoAkcWb89TyU$5f711eafb243c1c1a884715dd9bd6d185f29ccd3dab59ad19cc201a7260091cb', 'Mary', 'Jane', '127 Ice Cream Lane', 0, False])
        
        for uid in range(2, num_users):

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
            is_seller = uid in seller_ids #set to true if uid is in seller_ids


            #if is_seller:
            #    print(f"User {uid} is a seller")

            writer.writerow([uid, email, password, firstname, lastname, address, balance, is_seller])
        print(f'{num_users} generated')
    return

#id, seller_id, name, price, description, category, discount_code, prod_avg_rating, image_path, available
# def gen_products(num_products):
#     available_pids = []
#     categories = ['Fall', 'Winter', 'Spring', 'Summer'] 
#     with open('Products.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Products...', end=' ', flush=True)
#         for pid in range(num_products):
#             if pid % 100 == 0:
#                 print(f'{pid}', end=' ', flush=True)
#             creator_id = fake.random_int(min=1, max=(num_users-1))
#             name = fake.sentence(nb_words=4)[:-1]
#             price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
#             category = fake.random_element(elements=categories)
#             description = f"{category} inspired product: {fake.sentence(nb_words=8)}"
#             discount_code = None
#             prod_avg_rating = None
#             image_path = None 
#             available = fake.random_element(elements=('True', 'False'))
#             if available == 'True':
#                 available_pids.append(pid)
#             writer.writerow([pid, creator_id, name, price, description, category, discount_code, prod_avg_rating, image_path, available])
#         print(f'{num_products} generated; {len(available_pids)} available')
#     return available_pids


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

        with open("goodReviews.txt", "r") as f:
            positiveReview = f.read()

        with open("badReviews.txt", "r") as f:
            negativeReview = f.read()

        reviewModel = [positiveReview, negativeReview]

        for id in range(num_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            
            prod_or_seller = fake.random_int(min=0, max=1)
            
            if prod_or_seller == 0:
                pid = fake.random_int(min=0, max=num_products-1)
                seller_id = None
            else:
                pid = None
                seller_id = fake.random_int(min=0, max=num_users-1) # change to valid sellers once gen.py generates sellers

            # make sure that a user can only leave 1 review on a product
            pair = str(uid) + "," + str(pid)
            while pair in userProductPairs:
                pid = fake.random_int(min=0, max=num_products-1)
                pair = str(uid) + "," + str(pid)
            userProductPairs.add(pair)

            # randomly choose if it is gonna be a postive or negative review
            sentiment = fake.random_int(min=0, max=1)

            # generate rating based on sentiment
            if sentiment == 0: # positive   
                rating = fake.random_int(min=4, max=5)
            else: # negative
                rating = fake.random_int(min=0, max=3)

            # generate review based on randomly chosen sentiment
            text_model = markovify.Text(reviewModel[sentiment])
            review = text_model.make_sentence()

            while review is None:
                review = text_model.make_sentence()

            review = review.replace(",", "") # make sure there are no commas

            # randomly generate a time of creation
            time_posted = fake.date_time()
            time_modified = time_posted

            writer.writerow([id, uid, pid, seller_id, rating, review, time_posted, time_modified, 0])
        print(f'{num_reviews} generated')
    return

def gen_inventory(num_inventory, seller_ids):
    products_df = pd.read_csv('Products.csv', names=['pid', 'creator_id', 'name', 'price', 'description', 'category', 'discount_code', 'image_path', 'available'])
    joey_inventory_ids = [] #for demo purposes

    with open('Inventory.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        
        used_pairs = set()
        for inventory_id in range(num_inventory):
            if inventory_id % 10 == 0:
                print(f'{inventory_id}', end=' ', flush=True)

            # finding unique user_id, pid pairs
            user_id = random.choice(seller_ids)
            pid = fake.random_int(min=0, max=num_products - 1)

            temp = str(user_id) + "," + str(pid)

            while temp in used_pairs:
                pid = fake.random_int(min=0, max=num_products - 1)
                temp = str(user_id) + "," + str(pid)

            used_pairs.add(temp)

            shop_name = f"{fake.word()} Shop"
            seller_avg_rating = f'{fake.random_int(min=30, max=50) / 10:.2f}'  
            quantity_in_stock = fake.random_int(min=100, max=500)
            quantity_to_fulfill = fake.random_int(min=0, max=50)
            quantity_back_to_stock = fake.random_int(min=0, max=quantity_in_stock // 2)

            # Collect Joey's inventory IDs
            if user_id == 0:
                joey_inventory_ids.append(inventory_id)

            writer.writerow([inventory_id, user_id, pid, quantity_in_stock, quantity_to_fulfill, quantity_back_to_stock, shop_name, seller_avg_rating])
        
        print(f'{num_inventory} generated')
    return joey_inventory_ids

def gen_orders(num_orders):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        order_ids = []

        #ensure that first user has orders in order to demo
        min_joey_orders = 3
        num_orders_to_assign = min(num_orders, min_joey_orders)

        # Assign first min_joey_orders to Joey
        for order_id in range(num_orders_to_assign):
            if order_id % 10 == 0:
                print(f'{order_id}', end=' ', flush=True)
            uid = 0  # Joey's user_id
            total_price = f'{fake.random_int(min=20, max=500)}.{fake.random_int(0, 99):02}' 
            time_created = fake.date_time_this_year()
            time_fulfilled = None 
            writer.writerow([order_id, uid, total_price, time_created, time_fulfilled, None])
            order_ids.append(order_id)


        for order_id in range(num_orders_to_assign, num_orders):
            if order_id % 10 == 0:
                print(f'{order_id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)  
            total_price = f'{fake.random_int(min=20, max=500)}.{fake.random_int(0, 99):02}' 
            time_created = fake.date_time_this_year()
            time_fulfilled = None 
            writer.writerow([order_id, uid, total_price, time_created, time_fulfilled, None])
            order_ids.append(order_id) 
            
        print(f'{num_orders} generated')
    return order_ids

def gen_cart_items(num_cart_items, order_ids, joey_inventory_ids):
    with open('CartItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('CartItems...', end=' ', flush=True)
        # for every order, we choose a number 1-5 unique cart items
            # for x in range num: choose random quant, etc. and writer.write row cart item w/ associated order id
        number_cart_items = 0
        cart_id = 0
        for i in range(num_orders):
            num_citem = fake.random_int(min=1, max=5)
            for x in range(num_citem):
                quantity = fake.random_int(min=1, max=5)
                uid = fake.random_int(min=2, max=99)
                inv_id = fake.random_int(min=2, max=num_sellers - 1)
                time_created = fake.date_time_this_year()
                time_modified = fake.date_time_between_dates(datetime_start=time_created)
                order_id = i
                time_fulfilled = None
                is_fulfilled = False
                writer.writerow([cart_id, uid, inv_id, quantity, time_created, time_modified, order_id, time_fulfilled, is_fulfilled])
                number_cart_items += 1
                cart_id += 1
        # for cart_id in range(num_cart_items):
        #     if cart_id % 10 == 0:
        #         print(f'{cart_id}', end=' ', flush=True)
        #     uid = fake.random_int(min=0, max=num_users-1)  

            # # Assign the first 5 CartItems to include Joey's inventory
            # if cart_id < 5 and joey_inventory_ids:
            #     inv_id = random.choice(joey_inventory_ids)
            # else:
            #     inv_id = fake.random_int(min=0, max=num_inventory-1)  
            
            # #inv_id = fake.random_int(min=0, max=num_inventory-1)  
            # quantity = fake.random_int(min=1, max=10)  
            # time_created = fake.date_time_this_year()
            # time_modified = fake.date_time_between_dates(datetime_start=time_created)
            # # if fake.boolean(chance_of_getting_true=30):  # 30% chance of being part of an order
            # #     order_id = fake.random_element(elements=order_ids)
            # #     time_fulfilled = fake.date_time_between_dates(datetime_start=time_created) if fake.boolean(chance_of_getting_true=70) else None
            # # else:
            # #     order_id = None
            # #     time_fulfilled = None

            # # Find corresponding order_id if needed
            # if cart_id < len(order_ids):
            #     order_id = order_ids[cart_id]
            # else:
            #     order_id = None
        print(f'{number_cart_items} Cart Items generated')
    return

def gen_coupons(num_coupons):
    with open('Coupons.csv', 'w') as f:
        print('CartItems...', end=' ', flush=True)
        writer = get_csv_writer(f)
        for i in range(num_coupons):
            word = fake.word()
            discount = f'0.{fake.random_int(min=0, max=99):02}'
            writer.writerow([i, word, discount])
        return

gen_users(num_users, seller_ids)
# available_pids = gen_products(num_products)
available_pids = range(num_products)
gen_purchases(num_purchases, available_pids)
gen_reviews(num_reviews)
joey_inventory_ids = gen_inventory(num_inventory, seller_ids)
order_ids = gen_orders(num_orders)

# still Generate CartItems as normal, 
# just making sure joey's inventory is included for demo purposes
gen_cart_items(num_cart_items, order_ids, joey_inventory_ids)
gen_coupons(num_coupons)