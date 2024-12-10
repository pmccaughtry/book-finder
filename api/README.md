# Book Finder API

## Overview
This project utilizes FastAPI to perform book searches on behalf of clients. The search results are obtained from Google Books API.

## Set-up
1. From the project root directory (book-finder), [create a virtual environment](https://fastapi.tiangolo.com/virtual-environments/)
2. Activate the virtual environment: `source ./venv/bin/activate`

Note: If you receive an error creating a virtual environment you may need to install **venv**
`pip3 install venv` and then repeat steps 1. and 2. above.

## API Start-up
To start the Book Finder API *only*, run `npm run fastapi-dev` from the terminal in the project root directory (book-finder). This will install dependencies from requirements.txt and start the API in development mode.

## Testing
To test the files in this application run the following commands from the terminal:

1. If not in the application server directory: `cd book-finder/api`
2. Run tests: `pytest tests`

## API Endpoints
**/books** - returns JSON containing data related to the books that were searched (e.g., book cover, author information, book details)

**/health** - returns { 'status': 'OK' } if the server is running properly

**/health-details** returns details about uptime, cpu, and virtual memory

There is also a **catch-all** route to gracefully handle any non-existant routes, returning a 200 to mess with bots, bad actors, etc
