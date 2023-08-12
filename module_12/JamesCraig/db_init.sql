-- Reset datbase to clean slate to reset the values of all tables
DROP DATABASE IF EXISTS whatabook;
CREATE DATABASE whatabook;

USE whatabook;

DROP USER IF EXISTS 'whatabook_user'@'localhost';
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED BY 'MySQL8IsGreat!';
GRANT ALL PRIVILEGES ON whatabook.* TO 'whatabook_user'@'localhost';


-- Recreate the database tables with proper fields
CREATE TABLE user (
	user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(75) NOT NULL,
	last_name VARCHAR(75) NOT NULL
);

CREATE TABLE book (
	book_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	book_name VARCHAR(200) NOT NULL,
	details VARCHAR(500),
	author VARCHAR(200) NOT NULL
);

CREATE TABLE wishlist (
	wishlist_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	book_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(user_id),
	FOREIGN KEY (book_id) REFERENCES book(book_id)
);

CREATE TABLE store (
	store_id INT NOT NULL PRIMARY KEY,
	locale VARCHAR(500) NOT NULL
);
-- Repopulate database values with sample data.
INSERT INTO store (store_id, locale)
VALUES (2235, '1234 Elm Street, Lincoln, NE 68501');

INSERT INTO book (book_id, book_name, details, author)
VALUES 	(872465930, 'The Enigmatic Quest', 
		'A thrilling mystery that takes readers on a journey of unexpected twists and turns.', 
		'Victoria Westwood'),
		(582349106, 'Echoes of Eternity', 
		'A fantasy epic filled with magical creatures and a battle for the fate of a mythical world', 
		'Gabriel Stone'),
		(735190684, 'Whispers in the Wind', 
		'A poignant love story set in the 19th century amidst war and societal expectations', 
		'Isabelle Rivers'),
		(981756432, 'Beyond the Horizon', 
		'An adventurous tale of exploration, danger, and the search for the unknown.', 
		'Ethan Blackwood'),
		(609418753, 'Shadows of the Past', 
		'A gripping psychological thriller that delves into the depths of the human mind.', 
		'Amelia Knight'),
		(401257386, 'Stardust Dreams', 
		'A heartwarming story of dreams and aspirations set against the backdrop of a small town.', 
		'Oliver Moore'),
		(823694517, 'Infinite Possibilities', 
		'A thought-provoking exploration of the multiverse and the mysteries of existence.', 
		'Emily Davis'),
		(132567984, 'The Art of Serenity', 
		'A self-help guide to finding inner peace and harmony in a chaotic world.', 
		'Lucas Turner'),
		(450812673, 'Midnight Melodies', 
		'A collection of enchanting poems that celebrate love, nature, and the beauty of life.', 
		'Sophia Hart');

INSERT INTO user (user_id, first_name, last_name)
VALUES 	(7821, 'Emily', 'Johnson'),
		(3498, 'Benjamin', 'Clarke'),
		(5862, 'Sophia', 'Mitchell');

INSERT INTO wishlist (wishlist_id, user_id, book_id)
VALUES 	(286145, 7821, 401257386),
		(750812, 3498, 450812673),
		(912347, 5862, 582349106);