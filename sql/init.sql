CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, completed) VALUES
    ('Learn FastAPI', FALSE),
    ('Build an API', FALSE)
ON CONFLICT DO NOTHING;