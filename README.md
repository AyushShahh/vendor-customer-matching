# Vendor Customer Matching and Sales Tracking System
Website that tracks sales and matches vendors with customers based on their preferences.

## Installation
1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment
```bash
python -m venv .venv
```
4. Activate the virtual environment
```bash
.venv\Scripts\activate
```
5. Install the required packages
```bash
pip install -r requirements.txt
```
6. Make migrations and migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```
7. Run the server
```bash
python manage.py runserver
```