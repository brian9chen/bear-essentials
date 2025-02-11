-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.
 
CREATE TABLE Users (
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    balance DECIMAL DEFAULT 0,
    CHECK(balance >= 0),
    is_seller BOOLEAN DEFAULT FALSE
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    creator_id INT NOT NULL REFERENCES Users(id),
    name VARCHAR(255) NOT NULL,
    price DECIMAL(12,2),
    description TEXT,
    category VARCHAR(255) NOT NULL,
    discount_code VARCHAR(20),
    prod_avg_rating DECIMAL(12,2) DEFAULT 0,
    image_path VARCHAR(255) DEFAULT NULL,
    available BOOLEAN DEFAULT FALSE
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Inventory (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity_in_stock INT NOT NULL,
    quantity_to_fulfill INT NOT NULL,
    quantity_back_to_stock INT NOT NULL,
    shop_name VARCHAR(255) NOT NULL,
    seller_avg_rating DECIMAL(12,2)
);

CREATE TABLE Orders (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    total_price DECIMAL(12,2),
    time_created timestamp without time zone DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    time_fulfilled timestamp without time zone DEFAULT NULL
);

CREATE TABLE CartItems (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    inv_id INT NOT NULL REFERENCES Inventory(id),
    quantity INT NOT NULL,
    time_created timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    time_modified timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    order_id INT REFERENCES Orders(id),
    time_fulfilled timestamp without time zone DEFAULT NULL
);

CREATE TABLE Reviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    product_id INT REFERENCES Products(id),
    seller_id INT REFERENCES Users(id),
    rating DECIMAL(12,2),
    description TEXT,
    time_created TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    time_modified TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    num_upvotes INTEGER DEFAULT 0
);

CREATE TABLE Coupons (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    word VARCHAR(255) NOT NULL,
    discount DECIMAL(12,2) NOT NULL
)

ALTER TABLE CartItems ALTER COLUMN order_id DROP NOT NULL;
ALTER TABLE CartItems ADD COLUMN is_fulfilled BOOLEAN DEFAULT FALSE;
ALTER TABLE CartItems ADD COLUMN is_submitted;
ALTER TABLE Inventory ADD COLUMN image_path TEXT;
ALTER TABLE Orders ADD COLUMN coupon_id INT;

-- make sure there are no duplicates in inventory - there are some in customized csv, may have to manually remove them
ALTER TABLE Inventory ADD CONSTRAINT unique_user_product UNIQUE (user_id, pid);