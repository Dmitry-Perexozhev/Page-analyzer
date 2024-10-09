### Hexlet tests:
[![Actions Status](https://github.com/Dmitry-Perexozhev/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Dmitry-Perexozhev/python-project-83/actions)

### Page Analyzer

Page Analyzer is a Flask-based web application that enables users to evaluate the SEO performance of websites. It verifies site availability and examines key elements like headers, meta descriptions, and H1 tags.

### Key Features:

- Checks website availability.
- Analyzes title and meta description tags.
- Displays the analysis results through a user-friendly interface.

### Demo:

You can see the application in action by visiting this link: [Page Analyzer](https://python-project-83-amyh.onrender.com)
![last](https://github.com/user-attachments/assets/b3767de1-9be3-4103-9bc1-2f1394d1c9cd)

### Installation requirements
- Python 
- Poetry
- PostgreSQL
- Make

### Getting Started
#### Installation
1. Clone the project repository to your local device:
```
git clone git@github.com:Dmitry-Perexozhev/python-project-83.git
```
2. Go to the project directory:
```
cd python-project-83
```

3. Set up environment variables.
Open the `.env` file and replace the value of the SECRET_KEY and DATABASE_URL keys
- `SECRET_KEY`: a secret key for your application.
- `DATABASE_URL`: the connection string for your PostgreSQL database, formatted as `postgresql://username:password@localhost:5432/database_name`

4. Install the required dependencies using Poetry and make a migration. PostgreSQL must be running:
```
make build
```
#### Usage

Run local flask server
```
make dev
```
You can also run the server locally in development mode with the debugger active:
```
make debug
```
Run the production Gunicorn server

```
make start
```