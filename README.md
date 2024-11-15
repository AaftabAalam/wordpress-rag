# WordPress-Rag

WordPress-Rag is a full-stack web application built using React.js for the frontend, FastAPI for the backend, and integrated with WordPress. This project demonstrates how to combine these technologies to build a versatile web application that can handle natural language processing tasks, including summarization, text embeddings, and WordPress integration.

## Table of Contents
1. [Overview](#overview)
2. [Technologies](#technologies)
3. [Features](#features)
4. [Setup](#setup)
   1. [Backend Setup](#backend-setup)
   2. [Frontend Setup](#frontend-setup)
   3. [Running with Docker](#running-with-docker)
5. [Usage](#usage)
6. [License](#license)

## Overview
The `wordpress-rag` application is designed to integrate machine learning models with WordPress via FastAPI. The app includes two main components:
- **Frontend**: A React-based web interface.
- **Backend**: A FastAPI backend responsible for handling API requests related to text summarization, embeddings, integration with WordPress and using annoy indexing for indexing content.

## Technologies
- **Frontend**: React.js
- **Backend**: FastAPI, Uvicorn, Python
- **Machine Learning**: Python libraries for NLP, Summarization, and Embeddings (such as HuggingFace Transformers)
- **WordPress Integration**: WordPress REST API
- **Docker**: For containerization and simplified deployment

## Features
- **FastAPI Backend**: Handles API calls for text summarization, embedding generation, and WordPress integration.
- **React Frontend**: User-friendly interface to interact with the backend services.
- **WordPress Integration**: Fetch data from a WordPress site, process it, and display it via the frontend.
- **Dockerized Setup**: Fully containerized application for easier deployment and testing.

## Setup

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AaftabAalam/wordpress-rag.git
   cd wordpress-rag/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at `http://localhost:8000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd ../frontend
   ```

2. Install the necessary dependencies:
   ```bash
   npm install
   ```

3. Run the frontend development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`.

### Running with Docker
If you'd prefer to run the app using Docker, the project includes a `docker-compose.yml` file to orchestrate the containers.

1. Make sure you have Docker and Docker Compose installed.

2. Run the following command in the project root:
   ```bash
   docker-compose up
   ```

This will start both the frontend and backend services, which will be accessible at:
- **Frontend**: `http://localhost:3000`
- **Backend**: `http://localhost:8000`

## Usage
Once the application is running, navigate to `http://localhost:3000` in your browser to access the React frontend. You can interact with the backend via the API endpoints exposed by FastAPI for functionalities such as summarization, text embedding, and WordPress data retrieval.

## License
This code is proprietary. Unauthorized use, copying, modification, or distribution of this code is strictly prohibited.
