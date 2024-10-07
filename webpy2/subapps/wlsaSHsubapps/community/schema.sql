-- 创建表 users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    picture TEXT,
    description TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建表 posts
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建表 comments
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    parent_id INTEGER,
    quote_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_id) REFERENCES posts(id),
    FOREIGN KEY (quote_id) REFERENCES comments(id)
);

