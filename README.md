# Vendor Management System (VMS)

## Description

Welcome to the Vendor Management System (VMS), a Django-based application for managing vendor profiles, tracking purchase orders, and calculating vendor performance metrics. This system is built using Django and Django REST Framework to provide a scalable, modular, and efficient solution for vendor management.

## Core Features

- **Vendor Profile Management**: Create, retrieve, update, and delete vendor profiles.
- **Purchase Order Tracking**: Track purchase orders with details such as PO number, order date, items, quantity, and status.
- **Vendor Performance Evaluation**: Calculate performance metrics including on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## Additional Features

- **Scalable and Modular Code**: Follows MVC architecture and uses scalable code practices for easy maintenance and expansion.
- **Test Coverage**: Achieve full test coverage with end-to-end unit test cases.
- **REST API Documentation**: Implement Swagger for comprehensive API documentation and ease of understanding the code with proper documentation.
- **Data Model and Serialization**: Utilize data models and serializers for every REST API request to efficiently handle incoming requests.
- **Efficient Metric Calculation**: Implement efficient calculation methods for all performance metrics.
- **Database**: Use the built-in Django sqlite3 database for storing data securely.
- **Docker**: Implemented Docker.
- **Metrics Calculation**:
  1. **Fulfillment Rate**: Average of fulfilled POs (status 'completed' without issues) divided by the total number of POs issued to the vendor.
  2. **Response Time**: Average time difference between issue_date and acknowledgment_date for each PO.
  3. **Quality Rating**: Average of all quality_rating values for completed POs of the vendor.
  4. **On-Time Delivery Rate**: Percentage of completed POs delivered on or before the delivery date.

- **Token-based Authentication**: Implement token-based authentication for REST API access.
  - Example Tokens:
    1. "Token 1133f163e7cf13d8a647c1b4cddc3838d176459d"
    2. "Token 5d904d1d6cb37d04ff964ce650580ea8111394af"

## Installation

Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/sdeadarsh/vendor-management-system.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Makemigrations
   ```bash
   python manage.py makemigrations
   ```
   
4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the API documentation:
   Open a web browser and navigate to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) to access the Swagger documentation.

## Usage

- Use the provided APIs to manage vendor profiles and purchase orders.
- Authenticate users and obtain tokens for accessing protected endpoints.
- Explore the Swagger documentation for detailed API specifications and testing.
