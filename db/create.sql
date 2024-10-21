-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.
 
CREATE TABLE Users (
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    balance DECIMAL DEFAULT 0,
    CHECK(balance >= 0)
);

CREATE TABLE Sellers (
    id INT NOT NULL REFERENCES Users(id),
    shop_name VARCHAR(255) NOT NULL,
    seller_avg_rating DECIMAL(12,2)
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    creator_id INT DEFAULT NULL REFERENCES Users(id),
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2),
    description TEXT,
    -- SKU VARCHAR(255) NOT NULL, take out for now 
    category VARCHAR(255) NOT NULL,
    discount_code VARCHAR(20),
    prod_avg_rating DECIMAL(12,2) DEFAULT 0,
    image_path VARCHAR (255) DEFAULT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Carts (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    total_price DECIMAL(12,2),
    time_created timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    time_modified timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Inventory (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity_in_stock INT NOT NULL,
    quantity_to_fulfill INT NOT NULL,
    quantity_back_to_stock INT NOT NULL
);

CREATE TABLE CartItems (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    inv_id INT NOT NULL REFERENCES Inventory(id),
    quantity INT NOT NULL,
    time_created timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    time_modified timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);
