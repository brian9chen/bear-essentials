from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import markovify

num_users = 100
num_products = 2000
num_sellers = 100
num_purchases = 2500
num_reviews = 1000

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


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
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return

# def gen_sellers(num_sellers):
#     with open('Sellers.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Sellers...', end=' ', flush=True)
#         for sid in range(num_sellers):
#             writer.writerow([sid, shop_name, seller_avg_rating])
#         print(f'{num_sellers} generated')
#     return


def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, sellerid, name, price, description, category, discount_code, prod_avg_rating, image_path, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

#id, creator_id, name, price, description, category, discount_code, prod_avg_rating, image_path, available


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

        positiveReview = "I enjoyed this product and would recommend to others."
        negativeReview = "This product did not match my expectations and I would not buy it again."
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
            sentiment = random.randint(0, 1)

            # generate rating based on sentiment
            if sentiment == 0: # positive   
                rating = round(random.uniform(3, 5), 1)
            else: # negative
                rating = round(random.uniform(0, 3), 1)

            # generate review based on randomly chosen sentiment
            text_model = markovify.Text(reviewModel[sentiment])
            review = text_model.make_sentence()

            # randomly generate a time of creation
            time_posted = fake.date_time()
            time_modified = time_posted

            writer.writerow([id, uid, pid, rating, review, time_posted, time_modified])
        print(f'{num_reviews} generated')
    return


gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_reviews(num_reviews)
