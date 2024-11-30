# Kubernetes Query Agent

A natural language interface for querying Kubernetes cluster information.

## About The Project

This agent provides a simple way to query Kubernetes cluster information using natural language. It handles queries about nodes, pods, and deployments, returning clear, concise responses.

## Technical Implementation

- Built using FastAPI and Python 3.10
- Interfaces with Kubernetes using the official Python client
- Handles queries through a RESTful API endpoint
- Logging system for tracking queries and responses

### Query Types Supported:
1. Node count queries
2. Pod status checks
3. Deployment-Pod relationship queries

## Getting Started

### Prerequisites
* Python 3.10
* Minikube
* Kubernetes cluster (local or remote)
* kubectl configured

### Installation
1. Clone the repository:
```bash
git clone https://github.com/ShahDev007/query-agent-sample.git
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
.\venv\Scripts\activate   # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Agent
1. Start Minikube:
```bash
minikube start
```

2. Start the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

```bash
# Query Examples:
1. Node count:
   Query: "How many nodes are there in the cluster?"
   Response: "1"

2. Pod status:
   Query: "What is the status of pod 'nginx-pod'?"
   Response: "Running"

3. Deployment relationship:
   Query: "Which pod is spawned by my-deployment?"
   Response: "my-deployment-577d9fbfb9-jbwkj"
```

## Project Structure
- `main.py`: Core application logic
- `requirements.txt`: Project dependencies
- `agent.log`: Query logging
