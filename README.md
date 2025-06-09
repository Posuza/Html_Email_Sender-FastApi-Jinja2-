# FastAPI HTML App

This project is a simple web application built using FastAPI that serves HTML content.

## Project Structure

```
fastapi-html-app
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── routers
│   │   └── base.py      # Defines the routes for the application
│   └── templates
│       └── index.html   # HTML template served by the application
├── requirements.txt      # Lists the dependencies required for the project
├── .env                  # Contains environment variables for the application
└── README.md             # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-html-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

4. Open your browser and go to `http://127.0.0.1:8000` to see the application in action.

## Usage

This application serves a simple HTML page. You can modify the `index.html` file to change the content displayed on the web page.