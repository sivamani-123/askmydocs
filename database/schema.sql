-- AskMyDocs AI | MySQL 8 schema. Run in MySQL Workbench 8 (File > Open SQL Script > Run).
CREATE DATABASE IF NOT EXISTS documind CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE documind;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  full_name VARCHAR(120) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS documents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  filename VARCHAR(255) NOT NULL,
  category VARCHAR(60) NOT NULL DEFAULT 'Uncategorized',
  num_chunks INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS chunks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  document_id INT NOT NULL,
  user_id INT NOT NULL,
  chunk_index INT NOT NULL,
  text MEDIUMTEXT NOT NULL,
  embedding LONGBLOB NOT NULL,           -- float32 vector from sentence-transformers
  FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
  INDEX idx_chunks_user (user_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS chat_messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  question TEXT NOT NULL,
  answer MEDIUMTEXT NOT NULL,
  sources JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;
