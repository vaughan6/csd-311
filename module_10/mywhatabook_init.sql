/*
    Title: mywhatabook.init.sql
    Author: James Vaughan
    Date: 10 August 2023
    Description: WhatABook database initialization script.
*/

-- drop test user if exists 
DROP USER IF EXISTS 'whatabook_user'@'localhost';

-- create whatabook_user and grant them all privileges to the whatabook database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the whatabook database to user whatabook_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';

-- drop contstraints if they exist
ALTER TABLE wishlist DROP FOREIGN KEY fk_book;
ALTER TABLE wishlist DROP FOREIGN KEY fk_user;

-- drop tables if they exist
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS user;

/*
    Create table(s)
*/
CREATE TABLE store (
    store_id    INT             NOT NULL    AUTO_INCREMENT,
    locale      VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
);

CREATE TABLE book (
    book_id     INT             NOT NULL    AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    author      VARCHAR(200)    NOT NULL,
    details     VARCHAR(500),
    PRIMARY KEY(book_id)
);

CREATE TABLE user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(75) NOT NULL,
    last_name       VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id) 
);

CREATE TABLE wishlist (
    wishlist_id     INT         NOT NULL    AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    book_id         INT         NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
        REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
        REFERENCES user(user_Id)
);

/*
    insert store record 
*/
INSERT INTO store(locale)
    VALUES('1000 Galvin Rd S, Bellevue, NE 68005\n\tHours: Monday-Saturday: 9 AM - 6 PM, Sunday: 10 AM - 4 PM');

/*
    insert book records 
*/
INSERT INTO book(book_name, author, details)
    VALUES('Auto Biography of Narcissus', 'Narcissus', 'The longest auto-biography ever!');

INSERT INTO book(book_name, author, details)
    VALUES('The Adventures of Sir Procrastinator', 'Lazy McLazyface', 'Join Sir Procrastinator on his epic quest to avoid quests!');

INSERT INTO book(book_name, author, details)
    VALUES('How to Lose Weight by Eating Donuts', 'Doughnut Diver', 'Discover the secret diet plan that defies all logic!');

INSERT INTO book(book_name, details, author)
    VALUES('The Art of Snoring Like a Chainsaw', 'SnoozeMaster', 'Unlock your inner lumberjack with this snorevolutionary guide!');

INSERT INTO book(book_name, details, author)
    VALUES('101 Excuses for Every Occasion', 'Master Alibi', 'Never get caught empty-handed without an excuse again!');

INSERT INTO book(book_name, details, author)
    VALUES('The Great Journey of a Sofa Potato', 'Couch Captain', 'Join the epic adventure of a lifetime without ever leaving your couch!');

INSERT INTO book(book_name, details, author)
    VALUES('The Incredible Tales of Mr. Forgetful', 'ForgetMeNot', "A collection of stories you'll forget you read...wait, what was I saying?");

INSERT INTO book(book_name, details, author)
    VALUES('The Zen of Napping', 'Napoleon Snoozeapart', 'Achieve inner peace, one blissful nap at a time!');

INSERT INTO book(book_name, details, author)
    VALUES('The Amazing Power of Overthinking', 'Captain Overanalyze', 'Unleash the superpower of turning every simple decision into a grand dilemma!');

/*
    insert user
*/ 
INSERT INTO user(first_name, last_name) 
    VALUES('Trader', 'Joe');

INSERT INTO user(first_name, last_name)
    VALUES('Cookie', 'Monster');

INSERT INTO user(first_name, last_name)
    VALUES('Steve', 'Block');

/*
    insert wishlist records 
*/
INSERT INTO wishlist(user_id, book_id) 
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Cookie'), 
        (SELECT book_id FROM book WHERE book_name = 'How to Lose Weight by Eating Donuts')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Trader'),
        (SELECT book_id FROM book WHERE book_name = 'The Art of Snoring Like a Chainsaw')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Steve'),
        (SELECT book_id FROM book WHERE book_name = 'The Adventures of Sir Procrastinator')
    );
