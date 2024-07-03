# FoodMania API

This project is a backend API that provides food recommendations based on ingredients provided by the frontend. It is built using Flask, SQLAlchemy, MySQL, and Python.

# Features
* User registration and authentication
* Add, update, and delete food items
* Search for food items based on ingredients
* Daily food suggestions

# Technologies Used
* Python
* Flask: A lightweight WSGI web application framework
* SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library
* MySQL: A relational database management system
* Docker: To containerize the application (optional)

# Getting Started
These instructions will help you set up and run the project on your local machine for development and testing purposes.

# Prerequisites
* Python 3.10.12
* MySQL
* Docker (optional, for containerization)

# Installation
1. Clone the repository:
```bash
git clone https://github.com/seyyar95/FoodManiaBackend.git
cd FoodManiaBackend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the MySQL database:
* Create a new database:
```sql
CREATE DATABASE food_mania_db;
```
* Update the database connection details in the `models/engine/db_storage.py` file
```python
"mysql+pymysql://username:password@localhost:3306/food_mania_db"
```
Replace `username` and `password` with your MySQL credentials.

### Run the Application
```bash
python3 main.py
```
The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Authors
* Sayyar Heydarov - [Github](https://github.com/seyyar95)
* Gunay Gasimova - [Github](https://github.com/LGunay)
