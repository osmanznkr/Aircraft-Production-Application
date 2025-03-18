# Aircraft Production Application

## Overview
The Aircraft Production Application is designed to manage the production and inventory of aircraft components. It provides functionalities for creating, retrieving, listing, updating, and deleting various aircraft and inventory items. The application ensures that all inventory items are properly validated and tracked throughout the production process.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Django
- **Database**: PostgreSQL (or any other database supported by Django)
- **Authentication**: Django's built-in authentication system
- **Permissions**: Custom permission classes
- **Filtering**: Django Filter
- **Serialization**: Django REST Framework serializers
- **Signals**: Django signals for validation and state management
- **Audit Logging**: Django Auditlog

## Libraries Used
- **django**: The main web framework used for building the application.
- **psycopg2-binary**: PostgreSQL database adapter for Python, used to connect Django to a PostgreSQL database.
- **djangorestframework**: Toolkit for building Web APIs in Django.
- **drf-spectacular**: OpenAPI 3 schema generation for Django REST Framework.
- **environs**: Library for parsing environment variables.
- **drf-standardized-errors[openapi]**: Provides standardized error responses for Django REST Framework.
- **django-oauth-toolkit**: OAuth2 provider for Django and Django REST Framework.
- **django-filter**: Provides filtering capabilities for Django REST Framework.
- **django-auditlog**: Provides audit logging for Django models.

## Project Structure
- `models.py`: Contains the database models for User, Team, Profile, Aircraft, and Inventory.
- `views.py`: Contains the viewsets for managing aircraft and inventory items.
- `serializers.py`: Contains the serializers for converting model instances to JSON.
- `urls.py`: Contains the URL routing for the API endpoints.
- `signals.py`: Contains the signal handlers for validating and updating inventory items.
- `admin.py`: Registers the models with the Django admin site.
- `permissions.py`: Contains custom permission classes.
- `filtersets.py`: Contains filter classes for filtering querysets.
- `README.md`: Project documentation.

## Installation
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/aircraft-production-application.git
    cd aircraft-production-application
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create and set up the database**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage
1. **Access the admin site**:
    - Navigate to `http://127.0.0.1:8000/aircraft-admin`
    - Log in with the superuser credentials
    - Manage users, teams, profiles, aircraft, and inventory items

2. **API Endpoints**:
    - `GET /aircrafts/`: List all aircraft
    - `POST /aircrafts/`: Create a new aircraft
    - `GET /aircrafts/{serial_number}/`: Retrieve an aircraft by serial number
    - `PUT /aircrafts/{serial_number}/`: Update an aircraft by serial number
    - `GET /inventories/`: List all inventory items
    - `POST /inventories/`: Create a new inventory item
    - `GET /inventories/{serial_number}/`: Retrieve an inventory item by serial number
    - `DELETE /inventories/{serial_number}/`: Delete an inventory item by serial number
    - `GET /inventory-counts/`: List inventory counts

3. **Permissions**:
    - Only users with the appropriate permissions can create, update, or delete aircraft and inventory items.
    - Users can only manage inventory items associated with their own team.

## Contact
For any questions or inquiries, please contact [osmanznkr@gmail.com].