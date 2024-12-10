# Book Finder App

## Description
This application allows users to search the Google Books API via a Next.js app that consists of the front-end written in React, and the API server written with FastAPI.

## Project Set-up

1. Clone the repository from Github:
```bash
    # ssh
    git clone git@github.com:pmccaughtry/book-finder.git

    # https
    git clone https://github.com/pmccaughtry/book-finder.git
```

2. Create a virtual environment for the API
```bash
    # Step 1: go to the api directory
    cd api

    # Step 2: create the virtual environment
    python3 -m venv .venv

    # Step 3: activate the virtual environment
    source .venv/bin/activate
```
Note: If you receive errors creating a virtual environment you may need to install **venv** with `pip3 install venv` and then repeat steps 2. and 3. above.

3. Install NPM dependencies from the project root (book-finder): `npm install`

## Starting the Development Environment

### Client and API Start-up
`npm run dev` starts both the client and API concurrently.

### Client-only Start-up
`npm run next-dev`

### API-only Start-up
`npm run fastapi-dev`


```bash
# Any of the following commands can be used in place of the examples above.
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

### Application Hosts
> Client: localhost:3000
>
> API: localhost:8000

## API Endpoints
**/books** - returns JSON containing data related to the books that were searched (e.g., book cover, author information, book details)

**/health** - returns { 'status': 'OK' } if the server is running properly

**/health-details** returns details about uptime, cpu, and virtual memory

There is also a **catch-all** route to gracefully handle any non-existant routes, returning a 200 to mess with bots, bad actors, etc


### Disclosure
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/pages/api-reference/create-next-app).
