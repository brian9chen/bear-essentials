README - Bear Essentials

GitLab Repo: https://gitlab.oit.duke.edu/ksl48/mini-amazon-24-fall 

Team Members:
Brian Chen - Social Guru: responsible for Feedback / Messaging
Claire Luo - Users Guru: responsible for Account / Purchases
Hannah Wang - Sellers Guru: responsible for Inventory / Order Fulfillment
Kayla Liang - Carts Guru: responsible for Cart / Order
Kunling Tong - Products Guru: responsible for Products

Project Details:
We chose the standard project option (Mini-Amazon).
Our team/website name is Bear Essentials.

Our Work:
Brian Chen
    Met with all members to fork and set up the team GitLab repository and Google Drive folder, draft an E/R diagram for the website database, and plan individual next steps. 
    After the meeting, he focused on designing the relevant entities and relationships for the reviews feature and outlined these specifications in the Review table. 
    He worked on linking the Review entity with the users, sellers, and products, as well as outlining how the reviews feature will be integrated into the website in the Google Slides mockup of the website. 
    Finally, he described the constraints and assumptions of the Review entity in the REPORT PDF.
Claire Luo
    Claire met with all members to fork and set up the GitLab repository and Google Drive folder containing shared documents, draft an E/R diagram for the website database, and plan individual next steps.
    After the meeting, she designed the interface for the user internal profile view, public profile view, and purchases pages on the page-by-page Google Slides mockups.
    She also wrote up the description and logical flow for the user login, internal profile, and public profile pages.
    She helped work on the user flow and E/R diagram drawings. Finally, she outlined content for the README file.
Hannah Wang
    Hannah met with all members to fork and set up the team GitLab repository and Google Drive folder, draft an E/R diagram for the website database, and plan individual next steps.
    After the meeting, she focused on the inventory and order-fulfillment pages, adding bulleted descriptions, logical flow and diagrams to the page-by-page Google Slides mockup of the website.
    She also did final edits on the E/R diagram, and described the inventory and order-fulfillment related tables in the REPORT PDF.
    Finally, she outlined content for the README text file.
Kayla Liang
    Kayla met with all members to fork and set up the team GitLab repository and Google Drive folder, draft an E/R diagram for the website database, and plan individual next steps.
    After the meeting, she focused on the cart and order pages, adding bulleted information and diagrams to the page-by-page Google Slides mockup of the website.
    She also did final edits on the E/R diagram, and described the cart- and order-related tables in the REPORT PDF. Finally, she outlined content for the README text file.
Kunling Tong
    Kunling met with all members to fork and set up the team GitLab repository and Google Drive folder, draft an E/R diagram for the website database and plan individual next steps.
    After the meeting, she helped finalize and translate the E/R diagram into a logical and physical data model, and she also focused on the product pages.
    She designed the pages pertaining to general product information, adding products, and product reviews in the page-by-page Google Slides, and then described these tables in the REPORT PDF. 

Milestone 3 Additions:

Backend API Endpoints:

Users Guru:
 - db/create.sql
     - Updated the Users Table
 - db/data/Users.csv
     - Updated the csv to match the User schema in create.sql
 - app/__init__.py
     - Registered blueprint for purchases
 - app/model/purchase.py
     - Modified to add static method get_all_by_id to get info on purchases from Purchases table that have a certain uid
 - app/model/product.py
     - Added static method getPurchasesProducts, which gets a list of products and their details purchased by a specific user
 - app/purchases.py
     - Defines Blueprint named purchases 
     - Creates route for purchases page
     - Create API endpoint to get user purchases in JSON
 - app/templates/purchases.html
     - Created frontend page/widget to render table of purchases for a user_id inputted

Products Guru:
 - db/create.sql
     - Updated the Products Table 
 - db/data/CartItems.csv
     - Added attributes to Products.csv 
 - app/index.py
     - defining the /most_expensive_products route with def top_k
 - app/models/product.py
     - Updated product class 
     - Created def most_expensive_products 
 - app/templates/index.html
     - creating the frontend widget to enter k and get the k most expensive products

Carts Guru:
 - db/create.sql
     - creating CartItems table
 - db/load.sql
     - loading data from CartItems.csv file into CartItems table in database
 - db/data/CartItems.csv
     - test data for CartItems table in database
 - app/__init__.py
     - registered the blueprint for CartItems
 - app/cartitem.py
     - defining the /cartitem route
 - app/models/cartitem.py
     - defining the CartItem class and its methods
 - app/templates/cartitem.html
     - creating the frontend page showing the user’s cart

Sellers Guru:
 - db/create.sql
     - Creating the Inventory table
 - db/load.sql
     - Loading data from the Inventory.csv file into the Inventory table in the database
 - db/data/Inventory.csv
     - Testing the data for the Inventory table in the database
 - app/__init__.py
     - Registered the blueprint for Inventory
 - app/inventory.py
     - Defined the /inventory route 
 - app/models/inventory.py
     - Defining the Inventory class
 - app/templates/inventory.html
     - Creating the frontend page showing all products in the user’s inventory

Social Guru:
 - db/create.sql
     - Created the Reviews table
 - db/load.sql
     - Loaded data from the Reviews.csv file into the Review table in database
 - db/data/Reviews.csv
     - Created synthetic data to test the Reviews table in the database
 - app/__init__.py
     - Registered the Review blueprint
 - app/reviews.py
     - Defined two routes for handling user reviews in the web app:
         - /reviews
             - Fetches all reviews for the currently logged-in user
         - /reviews/<int:user_id>
             - Fetches the top 5 most recent reviews for the user with the specified user_id
 - app/models/review.py
     - Defined the Review class with the following methods:
         - constructor
             - Create a Review object
         - get(id)
             - Get a review by its id
         - get_all_by_uid(user_id)
             - Get all reviews by a user
         - get_5recent_reviews_by_uid(user_id)
             - Get top 5 most recent reviews by a user
 - app/templates/review.html
     - Created the frontend page to show a button next to each user that will take you to all of their reviews

Demo Video: https://drive.google.com/file/d/1QS7lCvNalI1q2NL1-6Jeg3v0WVc71H2H/view?usp=sharing 

Milestone 4 Additions

New Database
 - db/generated/gen.py
     - contains all of the functions used to generate randomized data in order to fill the csv files (listed below) and then populate our database
 - db/create.sql
     - contains the SQL functions to initialize our database schema
 - db/load.sql
     - contains the code to populate the database with the generated data in our csv files (listed below)
 - db/setup.sh
     - contains the code to run create.sql and load.sql in order to create our database schema and populate our database
 - db/generated/CartItems.csv
     - contains generated data about cart items in users’ carts
 - db/generated/Inventory.csv
     - contains generated data about the items in users’ inventories for users that are also sellers
 - db/generated/Products.csv
     - contains generated data about all of the products, both available and unavailable, that users can add to their carts
 - db/generated/Purchases.csv
     - contains generated data about a user’s purchases
 - db/generated/Reviews.csv
     - contains generated data about the reviews that have been made on various products by the users
 - db/generated/Users.csv
     - contains generated data about users: id, email, password, first and last name, address, and also an additional attribute is_seller

Demo Video:
https://drive.google.com/file/d/1imF42uUPAf9rzlQTkjQRRlHiRCMmkvV0/view?usp=sharing

