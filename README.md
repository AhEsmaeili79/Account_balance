# Account Balance Management System

## Overview

The **Account Balance Management System** is a comprehensive,Responsive web application built with Django that allows users to manage their financial transactions effectively. This system features a user-friendly dashboard, profile management, transaction tracking, custom and default categories, and detailed financial reporting. It utilizes Bootstrap for styling and JavaScript for enhanced interactivity.

### Features

- **Home Page**: Displays a financial chart summarizing your income and expenses along with sections for income and outcome.
- **User Authentication**: Sign up, sign in, and password recovery functionality. Password recovery uses email with a time-sensitive token.
- **Profile Management**: Update your first name, last name, and email.
- **Category Management**: Add custom categories and use default categories for organizing transactions.
- **Transaction Handling**: Record transactions with details such as amount, category, type (income or outcome), and date/time.
- **General Report**: View reports showing income and expenses by year, month, and category. Interactive charts on the home page link to detailed monthly reports.
- **Chart Report**: It's fully responsive and you can click on each month to see the details of that month with Income and Outcome.

## Installation

Follow these steps to set up and run the project:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/AmrhsnEs/Account_balance
    cd Account_balance
    ```

2. **Set Up a Virtual Environment**:
   Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the Database**:
   Edit the `settings.py` file to configure your database. You can choose between PostgreSQL or MySQL by updating the relevant settings.

5. **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the Application**:
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Configuration

- **Date Handling**: The application uses Shamsi (Jalali) dates, provided by the `django-jalali` package.
- **Email Configuration**: Email settings for password recovery are configured in `settings.py`.

## Screenshot

![Screenshot of Homepage](https://github.com/AmrhsnEs/Certificate/blob/main/screencapture-blnce-pythonanywhere-2024-08-25-22_24_30.png?raw=true)


![Screenshot of Transation](https://github.com/AmrhsnEs/Certificate/blob/main/screencapture-blnce-pythonanywhere-transactions-2024-08-25-22_25_08.png?raw=true)

![Screenshot of add Transation ](https://github.com/AmrhsnEs/Certificate/blob/main/screencapture-blnce-pythonanywhere-transactions-2024-08-25-22_26_10.png?raw=true)


![Screenshot of Categories](https://github.com/AmrhsnEs/Certificate/blob/main/screencapture-blnce-pythonanywhere-transactions-category-2024-08-25-22_25_51.png?raw=true)


![Screenshot of signup](https://github.com/AmrhsnEs/Certificate/blob/main/screencapture-blnce-pythonanywhere-accounts-signup-2024-08-25-22_29_33.png?raw=true)

![Screenshot of General Repost](https://github.com/AmrhsnEs/Certificate/blob/main/screencapture-blnce-pythonanywhere-reports-generalreport-2024-08-25-22_26_41.png?raw=true)




## Acknowledgments

- **Django**: High-level Python web framework used for development.
- **Bootstrap**: Framework for responsive design.
- **JavaScript**: Used for enhancing interactive features.
- **Persiantools**: For Persian date handling.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements or bug fixes.

## Contact

For further information or support, please open an issue on this repository or contact via [amrhsn.es@gmail.com](mailto:amrhsn.es@gmail.com).

