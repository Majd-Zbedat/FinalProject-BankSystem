# FinalProject-BankSystem
This repository contains the code of the Bank Management System
Bank Management System
JPMorgan Chase Bank has tasked us with building a comprehensive bank management API to handle customer accounts, transactions, loans, and more.

Table of Contents
Project Features
Requirements
Installation
Environment Variables
Running the Application
API Endpoints
Testing
Notes
Project Features
1. User Management
Create: Register new users with an email and password.
Update: Edit user details.
Delete: Remove user accounts.
2. Bank Accounts
Create: Open new accounts for users.
Suspend: Temporarily disable accounts.
Close: Permanently close accounts (if balance is non-negative).
3. Bank Account Operations
Deposit: Add funds to an account.
Withdraw: Deduct funds (respecting overdraft limits).
Balance Inquiry: Check current balance.
Transfer: Move funds between accounts.
Foreign Currency Support: Handle transactions in different currencies.
4. Loans
Grant Loan: Issue loans up to a specified limit.
Loan Repayment: Facilitate repayment of existing loans.
View Customer Loans: Retrieve loans associated with a user.
5. Profile Access
Authenticated Login: Secure login for customers to access their account and transaction details.
6. Transactions
Fee on Transactions: A fee is applied to each transaction (percentage can be customized).
Transaction History: Retrieve all transactions for each account.
Audit Account Operations: Every action (deposit, withdrawal, etc.) is recorded.
Requirements
Python 3.x
Django
Django REST Framework
Django REST Framework Simple JWT (for token-based authentication)
drf-spectacular (for API documentation)
Installation
Clone the repository:

bash
Copy code
git clone <repo_url>
cd <project_directory>
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables (see below).

Apply migrations:

bash
Copy code
python manage.py migrate
Create a superuser to access the admin dashboard:

bash
Copy code
python manage.py createsuperuser
Environment Variables
Create a .env file in the root directory and add the following:

plaintext
Copy code
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=your_database_url
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_email_password
Running the Application
Start the server with:

bash
Copy code
python manage.py runserver
API Endpoints
Endpoint	Description
/api/User/create/	Create a new user account
/api/User/create-token/	Obtain JWT token for authentication
/api/User/update/	Update user details
/api/BankAccount/	Manage bank accounts (create, suspend, close)
/api/BankAccount/deposit/	Deposit money into an account
/api/BankAccount/withdraw/	Withdraw money from an account
/api/BankAccount/transfer/	Transfer funds between accounts
/api/Transaction/	View and manage transactions
/api/Loan/	Manage loans (grant, repay, view)
/api/BankBalance/	Check the bank's total balance
Authentication
Use /api/User/create-token/ to obtain JWT tokens.
Pass the token as a Bearer token in the header for authenticated requests.
Swagger Documentation
Visit /swagger/ for the API documentation in Swagger UI.
