# FastAPI Thumbnail Feedback App

This project is a FastAPI application that accepts image uploads and provides feedback based on a thumbnail.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Docker Commands](#docker-commands)
- [Notes](#notes)
- [License](#license)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Create a .env file in the backend directory with the following content:**
GROQ_API_KEY=             # Your Groq API key. For more information, visit https://console.groq.com/login
DB_HOST=db
DB_USER=                  # Your database username
DB_PASSWORD=              # Your database password
DB_DATABASE=              # Your database name

3. **Build and start the Docker containers using the following command:**
docker-compose up --build

After the containers are up, the frontend will be accessible at http://localhost:5173/, and the FastAPI application will be available at http://localhost:8000.

**Usage**
**Navigate to the frontend URL (http://localhost:5173/).**
Use the file input to select an image.
Click the "Analyze Thumbnail" button to upload the image.
The application will provide feedback based on the uploaded thumbnail.

**Running & Testing the Backend only**
      If you want to test the backend using Postman:
**Open Postman and create a new request for backend testing only.**
Set the request type to POST.
Use the following URL: http://localhost:8000/upload_thumbnail/.
In the Body tab, select form-data.
Add a key named file (ensure the type is set to File).
Choose your image file and send the request.


**Docker Commands**
      **To rebuild the containers after making changes:**
               docker-compose up --build
      **To stop the containers:**
               docker-compose down
      **To view logs from the backend:**
             docker-compose logs backend

**Notes**
Ensure your database is set up correctly in the .env file.
If you encounter issues with the database connection, double-check your credentials and that the MySQL service is running.
If the database tables are not created, ensure your init_db.sql file is correctly placed in the backend directory.

**License**
This project is licensed under the MIT License. See the LICENSE file for more information.
