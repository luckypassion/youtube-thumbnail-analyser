CREATE TABLE IF NOT EXISTS thumbnail_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_hash VARCHAR(64) NOT NULL UNIQUE,
    score FLOAT,
    comment TEXT,
    original_image LONGBLOB,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
