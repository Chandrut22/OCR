# OCR-App

## Overview

This is a web application that allows users to upload images and extract text from them using OCR (Optical Character Recognition) technology. It also provides features for translating the extracted text and spell checking.

## Features

*   **User Authentication:** Secure signup, login, and logout functionality.
*   **Password Management:** Forgot password functionality with email verification.
*   **Image Upload:** Upload images in common formats (e.g., PNG, JPG).
*   **OCR Extraction:** Extracts text from uploaded images using the Gemini 2.0 Flash Lite model.
*   **Translation:** Translates extracted text into multiple languages.
*   **Spell Check:** Corrects spelling errors in the extracted text.
*   **File Management:** Allows users to delete uploaded files.

## Technologies Used

*   **Django:** A high-level Python web framework.
*   **Python:** The primary programming language.
*   **HTML, CSS, JavaScript:** For the frontend.
*   **pydantic-ai:** For interacting with the Gemini 2.0 Flash Lite model.
*   **googletrans:** For text translation.
*   **textblob:** For spell checking.
*   **MySQL:** As the database.
*   **Whitenoise:** For serving static files in production.
*   **dotenv:** For managing environment variables.

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd OCR-App
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate   # On Windows
    source venv/bin/activate  # On macOS and Linux
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    *   Create a `.env` file in the project root.
    *   Add the following variables, replacing the values with your actual credentials:

        ```
        SECRET_KEY=your_django_secret_key
        DEBUG=True or False
        DATABASE_NAME=your_database_name
        DATABASE_USER=your_database_user
        DATABASE_PASSWORD=your_database_password
        DATABASE_HOST=your_database_host
        DATABASE_PORT=your_database_port
        SENDER_MAIL_ID=your_email_address
        SENDER_PASSWORD=your_email_password
        ```

5.  **Configure the database:**

    *   Ensure MySQL is installed and running.
    *   Create a database with the name specified in your `.env` file.
    *   Run migrations:

        ```bash
        python manage.py migrate
        ```

6.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    *   Open your web browser and go to [http://127.0.0.1:8000/](http://_vscodecontentref_/0) to access the application.

## Deployment

1.  **Collect static files:**

    ```bash
    python manage.py collectstatic
    ```

2.  **Configure Whitenoise:**

    *   Ensure `whitenoise.middleware.WhiteNoiseMiddleware` is properly configured in [MIDDLEWARE](http://_vscodecontentref_/1) in [settings.py](http://_vscodecontentref_/2).
    *   Ensure [STATIC_ROOT](http://_vscodecontentref_/3) is set correctly in [settings.py](http://_vscodecontentref_/4).

3.  **Configure CSRF Trusted Origins:**
    *   Add your deployed application's URL to [CSRF_TRUSTED_ORIGINS](http://_vscodecontentref_/5) in [settings.py](http://_vscodecontentref_/6).

4.  **Deploy to a platform like Railway:**

    *   Follow the specific instructions for your chosen deployment platform.
    *   Make sure to set the environment variables in your deployment environment.

## Models
The project uses a custom user model `CustomUser` which extends Django's AbstractUser.

## Views
The project uses several views to handle different functionalities:
*   `index` - Renders the index page.
*   `login_view` - Handles user login.
*   `signup_view` - Handles user signup.
*   `upload` - Handles image uploads.
*   `output` - Displays the OCR output.
*   `delete_uploaded_file` - Handles deletion of uploaded files.
*   `translate_text` - Handles text translation.
*   `spell_check` - Handles spell checking.
*   `forgot_password` - Renders the forgot password page.
*   `send_verification_code` - Sends verification code to the user's email.
*   `verify_code` - Verifies the entered verification code.
*   `reset_password` - Resets the user's password.

## Static Files
The static files are located in the [`web/static`](d:\OCR\ezyZip\web\static) directory.

## Templates
The templates are located in the [`web/templates`](d:\OCR\ezyZip\web\templates) directory.

## URLs
The URLs are defined in the `web/urls.py` file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

