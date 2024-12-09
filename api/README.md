# Book Finder API

## Overview
This project utilizes FastAPI to perform books searches on behalf of clients. The book searches are obtained from Google Books API.

## Setup
Run the setup.sh (Linux/MacOS) or setup.ps1 (Windows) script from the project_root/scripts directory:

Linux example: `ilant-health-assessment/scripts/setup.sh`

If you are only interested in building the API run `ilant-health-assessment/scripts/api_setup.sh`

## Testing
To test the files in this application run the following commands from the terminal:

1. If not in the application server directory: `cd ilant-health-assessment/server`
2. Run tests: `pytest tests`

## API Endpoints
**/books** - returns JSON containing data related to the books that were searched (e.g., book cover, author information, book details)

**/health** - returns { 'status': 'OK' } if the server is running properly

**/health-details** returns details about uptime, cpu, and virtual memory

There is also a catch-all route to gracefully handle any non-existant routes, returning a 200 to mess with bots, bad actors, etc
