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
- **django-cors-headers**: Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS).

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
    git clone https://github.com/osmanznkr/aircraft-production-application.git
    cd aircraft-production-application
    ```

2. **Generate secret key for .env**:
    - Generate a new secret key using the following command:
        ```sh
        python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
        ```

3. **Edit .env file**:
    - Create a new `.env` file in the root directory of the project.
    - Add the following environment variables to the `.env` file:
        ```sh
        SECRET_KEY=your_secret_key
        DEBUG=True
        ALLOWED_HOSTS=127.0.0.1 localhost
        NAME=name
        USER=user
        PASSWORD=password
        RESOURCE_SERVER_INTROSPECTION_URL=http://127.0.0.1:8000/o/introspect/
        TOKEN_URL=http://127.0.0.1:8000/o/token/
       
      
4. **Run docker commands**:
    - Run dokcer compose commands:
        ```sh
        docker-compose up --build
        ```

5. **Create a superuser**:
    ```sh
    docker compose exec backend python manage.py createsuperuser
    ```

6. **Create password application for Oauth2**:
    - Navigate to `http://127.0.0.1:8000/aircraft-admin`
    - Log in with the superuser credentials
    - Create a new application with the following details:
        - Name: `Aircraft Production Application`
        - Client Type: `Confidential`
        - Authorization Grant Type: `Resource owner password-based`
        - Get the client id and client secret without saving them
        - Add the client id and client secret to the `.env` file:
            ```sh
            CLIENT_ID_TOKEN=password_flows_client_id
            CLIENT_SECRET_TOKEN=password_flows_client_secret
            ```
        - Save the application

7. **Create client application for Oauth2**:
    - Create a new application with the following details:
        - Name: `Aircraft Production Application`
        - Client Type: `Confidential`
        - Authorization Grant Type: `Credentials`
        - Get the client id and client secret without saving them
        - Add the client id and client secret to the `.env` file:
            ```sh
            CLIENT_ID=credentials_flows_client_id
            CLIENT_SECRET=credentials_flows_client_secret
            ```
        - Save the application

## Usage
1. **Access the admin site**:
    - Navigate to `http://127.0.0.1:8000/aircraft-admin`
    - Log in with the superuser credentials
    - Manage users, teams, profiles, aircraft, and inventory items
    - Create  all teams and assign users profiles to teams

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

3. **Set the permissions for users**:
    - Only users with the appropriate permissions can create, update, or delete aircraft and inventory items.
    - Users can only manage inventory items associated with their own team.
    - Inventory teams must have to these permissions to CRUD inventory items:
        - `Aircrafts | Inventory | Can change inventory`
        - `Aircrafts | Inventory | Can add inventory`
        - `Aircrafts | Inventory | Can delete inventory`
        - `Aircrafts | Inventory | Can view inventory`
      
    - Assembly teams must have to these permissions to CRUD aircraft items:
        - `Aircrafts | Aircraft | Can change aircraft`
        - `Aircrafts | Aircraft | Can add aircraft`
        - `Aircrafts | Aircraft | Can view aircraft` 
        - `Aircrafts | Inventory | Can view inventory`

    - Managers must have to these permissions to see aircraft and inventory items and manage users:
        - `Aircrafts | Aircraft | Can view aircraft`
        - `Aircrafts | Inventory | Can view inventory`
        - `Accounts | User | Can view User`

## Contact
For any questions or inquiries, please contact [osmanznkr@gmail.com].
