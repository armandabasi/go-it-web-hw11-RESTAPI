# Homework Assignment #11

The goal of this homework assignment is to create a REST API for storing and managing contacts. The API should be built using FastAPI framework and utilize SQLAlchemy for database management.

Contacts should be stored in the database and contain the following information:
- First Name
- Last Name
- Email
- Phone Number
- Birthday
- Additional Data (optional)

The API should have the following functionalities:
- Create a new contact
- Get a list of all contacts
- Get a contact by identifier
- Update an existing contact
- Delete a contact

In addition to the basic CRUD functionalities, the API should also have the following features:
- Contacts should be searchable by name, last name, or email address (Query).
- The API should be able to retrieve a list of contacts with birthdays in the next 7 days.

General Requirements:
- Use the FastAPI framework to create the API.
- Use the SQLAlchemy ORM for working with the database.
- Use PostgreSQL as the database.
- Support CRUD operations for contacts.
- Support storing the contact's birthday.
- Provide documentation for the API.
- Use the Pydantic data validation module.

