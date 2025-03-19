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

## How to works this project

1. Users can login to the system with their credentials.
   
![login](https://github.com/user-attachments/assets/bc18d070-2994-4de0-b740-15fd008992e7)

2. Inventory team members cannot view the manufactured aircraft list.

![wing-home](https://github.com/user-attachments/assets/9aa6ad08-aba6-4ae3-afe4-b8b16c412e6c)

3. People in inventory teams can only view and produce parts that their team has produced.

![wing-inventory](https://github.com/user-attachments/assets/cafe8b3b-5daf-44f9-a069-e84c70c5883a)

![wing-new-inventory](https://github.com/user-attachments/assets/e9cfd943-7455-49a7-a76d-ffaae5591c26)

4. The user can filter the parts produced in their team according to the aircraft and if the part is used, they can view the information on which aircraft it was used.

![wing-new-inventory](https://github.com/user-attachments/assets/1a354dca-9ad6-4ec4-871c-fb311fe32198)

![wing-detail](https://github.com/user-attachments/assets/cf107692-1d8b-4da2-a23f-afbecf3c83f2)

5. With advanced language support, the user can view data from the backend via the switch button at the top right of the navbar.

![wing-language-1](https://github.com/user-attachments/assets/e55f3ab8-04e6-461b-b11c-55daee4f52ac)

![wing-language-2](https://github.com/user-attachments/assets/50bac8ae-79ae-42d9-9553-e9f3172f1452)

6. The person in the assembly team can view the list of aircraft, see the inventories used, filter and assemble aircraft.

![assembly-home](https://github.com/user-attachments/assets/738c9141-0b4b-416d-b74a-81b3b60658d6)

![assembly-filter](https://github.com/user-attachments/assets/91ef3cd2-c227-4afa-87c1-c406e0c332ab)

![assembly-detail](https://github.com/user-attachments/assets/c40be0d0-57b8-420d-ab69-c272b52c94d1)

7. When assembling an airplane, the assembly team member displays the missing parts for the selected airplane.

![assembly-create-1](https://github.com/user-attachments/assets/16d30996-e6b4-4e6d-8dde-1ea7da57c19e)

![assembly-create-2](https://github.com/user-attachments/assets/117280fc-85e6-434f-a939-70d6c56cdd1a)

8. An employee in the assembly team is not authorized to create inventory and will receive an error if they do so.

![assembly-error](https://github.com/user-attachments/assets/86441ec2-6c09-4177-a583-fae82999f14e)

9. An employee in the assembly team displays all the stocks, filters the stocks and dynamically displays all the data such as how many parts of which airplane, how many parts are used, how many are ready for use.

![assembly-stocks-1](https://github.com/user-attachments/assets/31fbb85e-8a3e-4762-a6b0-34b6e0e52a2f)

![assembly-stocks-2](https://github.com/user-attachments/assets/70132a3c-3629-4e5c-94d9-1949840e577a)


10.A person with managerial authority displays the employees and how many employees are on which team and how many people work on which team.

![manager-1](https://github.com/user-attachments/assets/3cfe4a50-0b2e-449d-a8ec-a5ba9eee9a60)

![manager-3](https://github.com/user-attachments/assets/a165f3b1-ee93-41cc-be36-af8ee4c4f043)













## Contact
For any questions or inquiries, please contact [osmanznkr@gmail.com].

