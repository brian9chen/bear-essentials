# Bear Essentials.

Originally created by [Rickard
Stureborg](http://www.rickard.stureborg.com) and [Yihao
Hu](https://www.linkedin.com/in/yihaoh/) for CS 316 Fall 2021 at Duke University.  Amended by
various teaching staff in subsequent years.

## Team
Brian Chen - responsible for Feedback / Messaging
Claire Luo - responsible for Account / Purchases
Hannah Wang - responsible for Inventory / Order Fulfillment
Kayla Liang - responsible for Cart / Order
Kunling Tong - responsible for Products

## Description

This project is a comprehensive e-commerce platform designed to support a wide range of user, product, review, and order management functionalities. Below is a detailed list of implemented or attempted features, categorized by functionality and their statuses.

## Features

### Reviews
Users can submit and manage reviews for both products and sellers. Each user is limited to one review per product or seller, with the option to edit or delete their reviews from their profile. Reviews include upvote and downvote functionality, allowing logged-in users to provide feedback on others’ reviews. Product and seller pages display average ratings and the total number of reviews, with reviews sorted by upvotes for easy visibility.

### Users
Users can create accounts, log in, and manage their profiles by updating details such as their name, email, address, and password. Each user starts with a balance they can add to or withdraw from, which is used for purchases. Users can browse their purchase history, view public profiles of other users, and see seller details associated with specific products. Format validation ensures inputs like email addresses are correct.

### Products
The platform supports browsing and searching for products by name, description, category, price, and rating. Each product includes detailed attributes such as a name, description, image, price, and average review rating. Sellers can add new products or add existing products to their inventory. Only the original creator of a product can edit its attributes, while other sellers can adjust quantities. Products are tagged as "Best Sellers" if they fall within the top 10% by purchases, with sorting options that include price, name, rating, and bestseller status.

### Cart and Orders
Users can add items to their cart by selecting a seller and quantity, with validations to ensure inputs are within stock limits and are positive integers. The cart page provides an overview of selected items, their prices, and available actions such as removing items, changing quantities, and applying coupon codes. Orders update inventories and user balances upon submission and include a fulfillment workflow for sellers, who can manage and track order status. The past orders page and individual order pages provide detailed breakdowns of purchases, including fulfillment statuses and applied discounts.

### Inventory Management
Sellers can manage their inventory by adding new products or incorporating existing products already listed on the platform. A search feature helps sellers find products by name and category. Once added, sellers can adjust stock quantities, and product creators can edit additional attributes like price and description. Inventory updates ensure that duplicate products cannot be added, maintaining consistency across the platform.

### Data and Security
The project uses synthetically generated realistic data for users, products, sellers, purchases, reviews, and orders, with a focus on realism in product descriptions, images, and review text. Security measures include parameterized SQL queries to prevent injection attacks and carefully validated user inputs. Demonstration users and manually created reviews showcase key features and support testing scenarios.

## Instructions

1. Fork this repo by clicking
   the small 'Fork' button at the very top right on GitLab.
   In your newly forked repo, find the blue "Clone" button.  Copy the
   "Clone with SSH" text.

2. In your container shell, issue the command `git clone
   THE_TEXT_YOU_JUST_COPIED` (make sure to replace
   `THE_TEXT_YOU_JUST_COPIED` with the "Clone with SSH" text).
   
3. In your container shell, change into the repository directory and
   then run `./install.sh`.  This will install a bunch of things, set
   up an important file called `.flashenv`, and creates a simple
   PostgreSQL database named `amazon`.

## Running/Stopping the Website

To run your website, in your container shell, go into the repository
directory and issue the following commands:
```
poetry shell
flask run
```

The first command ensures that you are in the correct Python virtual
environment managed by a tool called `poetry` (you can tell that your
command-line prompt looks differently --- it would start with the name
of the environment).  The second command runs the Flask/web server.
Do NOT run Flask outside the `poetry` environment; you will get
errors.

You can now use your laptop's browser to explore the website. Point your browser to
http://localhost:8080/

To stop your app, type <kbd>CTRL</kbd>-<kbd>C</kbd> in the container
shell; that will take you back to the command-line prompt, still
inside the `poetry` environment. If you are all done with this app for
now, you can type `exit` to get out of the `poetry` environment and
get back to the normal container shell.

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `amazon`
behind the scene.  As part of the installation procedure above, this
database has been created automatically for you.  You can access the
database directly by running the command `psql amazon` in your VM.

For debugging, you can access the database while the Flask server is
running.  We recommend you open a second container shell to run `psql
amazon`.  After you perform some action on the website, you run a
query inside `psql` to see the action has the intended effect on the
database.

The `db/` subdirectory of this repository contains files useful for
(re-)initializing the database if needed.  To (re-)initialize the
database, first make sure that you are NOT running your Flask server
or any `psql` sessions; then, from your repository directory, run
`db/setup.sh`.

* You will see lots of text flying by --- make sure you go through
  them carefully and verify there was no errors.  Any error in
  (re-)initializing the database will cause your Flask server to fail,
  so make sure you fix them.

* If you get `ERROR: database "amazon" is being accessed by other
  users`, that means you likely have Flask or another `psql` still
  running; terminate them and re-run `db/setup.sh`.  If you cannot
  seem to find where you are running them, a sure way to get rid of
  them is to stop/start your container.

To change the database schema, modify `db/create.sql` and
`db/load.sql` as needed.  Make sure you run `db/setup.sh` to reflect
the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to
initialize the database contents when you run `db/setup.sh`.  Under
`db/generated/`, you will find alternate CSV files that will be used
to initialize a bigger database instance when you run `db/setup.sh
generated`; these files are automatically generated by running a
script (which you can re-run by going inside `db/data/generated/` and
running `python gen.py`.

* Note that PostgreSQL does NOT store data inside these CSV files; it
  store data on disk files using an efficient, binary format.  In
  other words, if you change your database contents through your
  website or through `psql`, you will NOT see these changes reflected
  in these CSV files (but you can see them through `psql amazon`).

* For safety, a database should never store password in plain text;
  instead it stores one-way hash of the password.  This rule applies
  to the password value in the CSV files too.  To see what hashed
  password value you should put in a CSV file, see `db/data/gen.py`
  for example of how to compute the hashed value.

## Note on Hiding Credentials

Use the file `.flaskenv` for passwords/secret keys --- we are talking
about passwords used to access your database server, for example (not
user passwords for your website in CSV files for loading sample
database).  This file is NOT tracked by `git` and it was automatically
generated when you first ran `./install.sh`.  Don't check it into
`git` because your credentials would be exposed to everybody on GitLab
if you are not careful.
