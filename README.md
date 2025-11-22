## Stetps to run server in development environment

1. **Create a Virtual Environment** (if not already created):
    ```bash
    python -m venv venv
    ```

1. **Activate the Virtual Environment**:
    On Windows
    ```bash
    .\venv\Scripts\activate
    ```

1. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
1. **Navigate to Source Directory**:
   ```bash
   cd ./src
   ```
1. **Update the Database Migrations for all Apps**:
   ```bash
   python manage.py makemigrations
   ```
1. **Apply Database Migrations**:
    ```bash
    python manage.py migrate
    ```

1. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

1. **Run the Development Server**:
    ```bash
    python manage.py run server
    ```