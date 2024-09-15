DROP TABLE urls, url_checks;

CREATE TABLE urls(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at date
);


CREATE TABLE url_checks(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id INT,
    status_code INT,
    h1 varchar(255),
    title TEXT,
    description TEXT,
    created_at date
);