# Cynerio's Assignment:
Web server that implements a checkin/checkout process for users.
# Technologies Used:
FastAPI, Vue, Vuetify, Vite
# Project Structure:
- task_manager
    - alembic - database migration management
    - api - route handlers
    - schemas - the data schemas for serialization, validation, etc.
    - services - the business logic
    - tests - tests
    - dependencies.py - data dependencies inject into route handlers and services
    - requirements - list of required libraries
    - main.py - entry point
- client
    - components - the used components
    - main.js - entry point
# How to run the code
Task Manager:
```
uvicorn task_manager.main:app --reload
```

Client:
Run the following command:
```
npm run dev
```

Docker (TBD):
Open a terminal in the directory containing your docker-compose.yml file and run the following command:
```
docker-compose up --build
```
To stop the containers, press Ctrl + C in the terminal, and then run:
```
docker-compose down
```
# Usage Guide:
Swagger UI allows development team to visualize and interact with the API's resources.
Available when project is running at: http://127.0.0.1:8000/docs

Frontend client is available at: http://127.0.0.1:8080/

# Testing:
To run the tests:
```
pytest
```
# To be done list:
- task_manager:
    - Create an exception handler service
    - Add additional tests (services, etc.)
    - Work with containerized database
    - Configure a test database that rollback data after testing
    - Transaction decorator
    - Environment variables
    - Black (clean code)
    - Typing and pylint    
- client:
    - Complete the requirements
    - Statful and stateless components separation
    - CSS ans style
    - Environment variables
    - Service handler for API calls
    - Error handler
    - Tests
    - Typescript
