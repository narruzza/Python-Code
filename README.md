# MyTracker

MyTracker is a web application designed to help you track and manage your tasks efficiently. With a user-friendly interface and powerful features, MyTracker makes it easy to stay organized and productive.

## Features

- Task creation and management
- Due date reminders
- Categorization and tagging
- Progress tracking
- User authentication

## Installation

To install and run MyTracker locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/MyTracker.git
    cd MyTracker
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. Open your web browser and go to `http://127.0.0.1:8000` to start using MyTracker.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

If you have any questions or feedback, feel free to reach out to us at [narruzza@student.saintaug.nsw.edu.au](mailto:narruzza@student.saintaug.nsw.edu.au).
