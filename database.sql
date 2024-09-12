DROP TABLE urls;

CREATE TABLE urls(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at date
);