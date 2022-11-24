# Sample FastAPI + GraphQL Book API Project 
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/EdyVision/pii-codex/graphs/commit-activity)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)


A sample python book-api project using FastAPI and GraphQL. This project leverages docker for containerization and provides the full setup to deploy to AWS Fargate using AWS CDK. The starter is created for and used in the <a href="https://www.amazon.com/dp/B09Z7CSDRX">Building Serverless Python Apps Using FastAPI and AWS</a> book by <a href="https://eidanrosado.com">Eidan J. Rosado</a>.

### Running Services with Docker
To avoid setting up MongoDB and other such services locally, the team uses Docker. You'll need to install Docker to proceed pulling the image from the team's hub. Contact one of the team admins for access to the hub. To start peripheral services simply execute the following:

```bash
docker-compose up
```

To refresh the image on your local (for server devs), run the following: 

```bash
docker build -t bookapi -f Dockerfile .
```

You can run the one off image and container with the following:

```bash
docker run -d --name bookapi -p 8000:8000 bookapi
```

### Running API Locally
You'll need the following environment variables configured or in a .env file to run the server successfully:

```bash
# FastAPI Setup
export HOST="127.0.0.1"
export PORT=8000

# BookAPI DB Setup
export DB_URL='mongodb://localhost:27017'
export DB_NAME='bookapi'

# AWS and Infra Setup
AWS_ACCOUNT='YOUR_ACCOUNT'
AWS_REGION='AWS REGION (e.g. us-east-1)'
DOMAIN_NAME='example.com'

# Infra Setup
LOCAL_NETWORK_CIDR='YOUR_NETWORK_CIDR'
```

The main entry point is main.py, so you can start that file from command line or use whatever execution method is available from your IDE. To install the IDE to interact with GraphQL, look in the SETUP.md for GraphQL Playground installation instructions then simply open the GraphQL Playground to interact with the local server and insert the base url http://127.0.0.1:8000/graph.

## Dev Notes
### Viewing Changes
Changes under /app may be picked up by the auto-refresh (no need to restart server). To understand how to use the playground to run queries, please reference the following: <a href="https://graphql.org/learn/queries/">GraphQL Queries Reference</a>

### Running Tests
All tests are located under the <em>tests</em> folder. To run them from terminal, execute the following:

```bash
pytest tests
```

To run with coverage, run the following:

```bash
coverage run -m pytest -v tests && coverage report -m
```

### Using the Makefile
Note that the Makefile included in this repo uses several environment variables. Be sure to have your .env setup to fully leverage all the shortcuts made available.

