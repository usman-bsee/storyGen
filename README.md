# GitHub Model Project

## Introduction

This project is a comprehensive implementation designed to facilitate various functionalities related to model loading, character generation, scene generation, and more. It includes multiple scripts and configuration files to streamline these processes.

## Installation

To get started with this project, you need to clone the repository and install the required dependencies. Follow the steps below:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/githubModelProject.git
    cd githubModelProject
    ```

2. **Set up a conda environment:**
    ```bash
    conda create -n storyGen python=3.12
    conda activate storyGen
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **How to Setup Redis Server:**

    Check the `REDIS-SETUP-README` file for more details.

5. **How to Setup Celery Worker:**

    Check the `CELERY-SETUP-README` file for more details.

## Usage

Redis server and Celery worker have been designed for this application. You need to start the Redis server, Celery worker, and Flask application to initiate this system.

To start the Redis server, follow the `REDIS-SETUP-README` file for setup instructions. Once setup is complete, use this command to start the Flask application on the server machine:

```bash
python server_app.py

