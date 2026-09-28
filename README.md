# Fraud Transaction Review System

## SDC480 Software Development Capstone

**Student:** Christopher Lyles  
**Project:** Fraud Transaction Review System  
**Current Development Phase:** Phase #3

---

## Project Overview

The Fraud Transaction Review System is a web-based application designed to provide fraud analysts with a centralized workflow for reviewing potentially suspicious financial transactions.

The application allows an analyst to securely log in, view transactions requiring investigation, examine transaction details, document review decisions, search transaction records, maintain an audit history of completed investigations, and manage transaction data.

The application is being developed incrementally throughout the SDC480 Software Development Capstone. Each phase builds upon the functionality completed during the previous phase.

---

## Phase #1 – Initial Application Foundation

Phase #1 established the initial working version of the Fraud Transaction Review System.

### Phase #1 Features

- Secure analyst login
- Fraud operations dashboard
- Pending transaction count
- High-risk transaction count
- Completed review count
- Transaction review queue
- Individual transaction details
- Analyst review workflow
- Fraud decision documentation
- Review history and audit trail
- SQLite database integration

Phase #1 established the core fraud-review workflow and database-backed application structure.

---

## Phase #2 – Design and Application Development

Phase #2 expanded the initial application and continued development of the website and database functionality.

### Phase #2 Functionality

- Continued development of the web application interface
- Navigation between application pages
- Functional analyst login
- User information stored in the SQLite database
- Fraud operations dashboard
- Transaction review queue
- Individual transaction detail pages
- Analyst review workflow
- Review history
- Database-backed application data
- Continued interface and application design improvements

Phase #2 established a more complete working website and demonstrated continued development of the application's interface, database, and fraud-review workflow.

---

## Phase #3 – Search, Data Management, and Security

Phase #3 builds upon the previous phases by adding transaction search functionality, transaction data-management capabilities, additional input validation, and account-security functionality.

### Transaction Search

The application provides a dedicated Search Transactions page.

Transactions can be searched by:

- Account ID
- Merchant
- Location
- Transaction type
- Status

Partial searches are supported, allowing an analyst to enter only part of a value rather than the complete search term.

Search results display the matching transaction records and provide access to transaction-management actions.

### Transaction Data Management

Phase #3 includes CRUD functionality for transaction records:

- Create new transaction records
- Read and search transaction records
- Update existing transaction records
- Delete transaction records
- Confirmation before deletion

### Input Validation

The transaction-management functionality includes validation controls such as:

- Required fields
- Transaction amount must be zero or greater
- Fraud score must be between 0 and 100
- Controlled transaction-type selections
- Controlled transaction-status selections

These controls help prevent invalid transaction data from being submitted to the database.

### Account and Password Security

The application includes account-security controls such as:

- Authenticated access to protected application pages
- Password hashing
- Current-password verification before changing a password
- New-password confirmation
- Password-complexity requirements

Password requirements include:

- At least 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Fraud Review and Audit Functionality

The existing fraud-review workflow remains integrated with Phase #3.

Analysts can:

- View transactions prioritized by fraud risk score
- Open individual transaction details
- Record an analyst review decision
- Enter analyst notes
- Submit completed reviews
- View completed reviews in the Fraud Review History
- Maintain an audit trail showing the analyst and review date/time

---

## Technologies Used

- Python 3
- Flask
- SQLite
- HTML
- CSS
- Git
- GitHub

---

## Application Structure

- `app.py` – Current Flask application and primary source code
- `fraud_review.db` – SQLite database containing application data
- `app_phase1_backup.py` – Backup of the Phase #1 application
- `app_phase2_backup.py` – Backup of the Phase #2 application
- `README.md` – Project documentation
- `templates/` – Reserved for external HTML templates
- `static/` – Reserved for external static resources

### Source Code Organization

The current application is implemented primarily in `app.py`.

The file contains the Flask routes and primary application logic, including authentication, database operations, page rendering, transaction review functionality, search functionality, CRUD operations, input validation, password-management functionality, and dynamically generated HTML/CSS.

The `templates` and `static` directories are currently reserved for future separation of HTML templates and static resources if the application is further refactored.

The phase backup files preserve earlier versions of the source code and provide evidence of the application's incremental development.

---

## Running the Application

1. Install Python and Flask.
2. Open a command prompt, terminal, or Anaconda Prompt.
3. Navigate to the project directory.
4. Run:

   `python app.py`

5. Open a web browser and navigate to:

   `http://127.0.0.1:5000`

---

## Phase #3 Functional Testing

The current application has been tested for the following functionality:

- Successful authenticated login
- Dashboard statistics
- Transaction review queue
- Individual transaction details
- Analyst review submission
- Completed review history
- Transaction searching
- Partial transaction searching
- Adding a transaction
- Editing a transaction
- Deleting a transaction
- Delete confirmation
- Required-field validation
- Transaction amount validation
- Fraud score validation
- Password-management functionality

---

## Current Project Status

Phase #3 provides a functional expansion of the Fraud Transaction Review System while preserving the functionality developed during Phases #1 and #2.

The current application supports authentication, dashboard statistics, transaction review, analyst decisions, audit history, transaction searching, transaction CRUD operations, input validation, password security, and SQLite database integration.

Development will continue in subsequent phases of the SDC480 Software Development Capstone.