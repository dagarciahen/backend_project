CREATE TABLE IF NOT EXISTS reviewers(
    reviewer_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    joined_at DATE NOT NULL DEFAULT (CURRENT_DATE)

);

CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    reviewer_id INT NOT NULL,
    book_id INT NOT NULL,
    comment TEXT NOT NULL,
    rating TINYINT NOT NULL CHECK(rating BETWEEN 1 AND 5),
    status ENUM('pending', 'processing', 'processed') NOT NULL DEFAULT 'pending',
    review_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    FOREIGN KEY (reviewer_id) REFERENCES reviewers(reviewer_id)

);

INSERT INTO reviewers(username, email, password_hash)
VALUES (
    'daniel',
    'test@example.com',
    'ebf0af4f7b054f2858bbfcab58776ee0:ca9169c244248142c5aa052807a2023b65fb4440b753638addadba5367d4e902' -- (password123)
);