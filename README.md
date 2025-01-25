### Hexlet tests:
[![Actions Status](https://github.com/Dmitry-Perexozhev/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Dmitry-Perexozhev/python-project-83/actions)

### Page Analyzer

Page Analyzer is a Flask-based web application that enables users to evaluate the SEO performance of websites. It verifies site availability and examines key elements like headers, meta descriptions, and H1 tags.

### Key Features:

- Checks website availability.
- Analyzes title and meta description tags.
- Displays the analysis results through a user-friendly interface.

### Demo:

You can see the application in action by visiting this link: <a href="http://194.87.99.31:5000/" target="_blank">Page Analyzer</a>

![demo](https://github.com/user-attachments/assets/22f5a0e0-4e7b-4982-82bc-ef9a21072308)

### Installation requirements

- Python 
- Poetry
- PostgreSQL
- Make

### Getting Started
#### Installation 

1) Clone the project repository to your local device:
```
git clone git@github.com:Dmitry-Perexozhev/python-project-83.git
```
2) Go to the project directory:
```
cd python-project-83
```
3) Standard installation<br>
Create the .env file and set up values for environment variables:<br>
- **`SECRET_KEY`**: a secret key for your application.
- **`DATABASE_URL_dev`**: the connection string for your PostgreSQL database, formatted as `postgresql://username:password@localhost:5432/database_name`
- **`DEBUG`**: True<br>
Install the required dependencies using Poetry and make a migration. PostgreSQL must be running:
```
make build
```
4) Installation using Docker<br>
Install Docker and Docker Compose<br>
Create the .env file and set up values for environment variables:<br>
- **`SECRET_KEY`**: a secret key for your application.
- **`DATABASE_URL_deploy`**: the connection string for your PostgreSQL database, formatted as `postgresql://username:password@localhost:5432/database_name`
- **`DEBUG`**: False
- **`POSTGRES_USER`**: postgres username 
- **`POSTGRES_PASSWORD`**: user password
- **`POSTGRES_DB`**: name database<br>
Build the app. Gunicorn server is in use:
```
docker-compose up --build -d
```

#### Usage for standart installation

- Run local flask server
```
make dev
```
- You can also run the server locally in development mode with the debugger active:
```
make debug
```
- Run the production Gunicorn server
```
make start
```