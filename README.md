<a name="readme-top" id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#query-examples">Query Examples</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project implements a Kubernetes Query Agent that can answer natural language queries about applications deployed on a Kubernetes cluster. The agent provides a simple REST API endpoint that accepts queries and returns information about pods, deployments, and cluster status.

### Built With

* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)
* ![Kubernetes](https://img.shields.io/badge/kubernetes-326ce5.svg?&style=for-the-badge&logo=kubernetes&logoColor=white)

## Getting Started

### Prerequisites

* Python 3.10
* Minikube
* kubectl
* A running Kubernetes cluster (local or remote)

### Installation

1. Clone the repository
```sh
git clone https://github.com/ShahDev007/query-agent-sample.git
```

2. Create and activate virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Linux/Mac
.\venv\Scripts\activate   # On Windows
```

3. Install required packages
```sh
pip install -r requirements.txt
```

4. Start Minikube
```sh
minikube start
```

5. Start the server
```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Usage

The agent accepts POST requests to `/query` endpoint with a JSON body containing your query:

```json
{
    "query": "How many nodes are there in the cluster?"
}
```

## Query Examples

1. Check number of nodes:
```powershell
$body = @{
    "query" = "How many nodes are there in the cluster?"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/query" -Method Post -ContentType "application/json" -Body $body
```
Response:
```
There are 1 nodes in the cluster
```

2. Check pod status:
```powershell
$body = @{
    "query" = "What is the status of pod 'nginx-676b6c5bbc-kpftf'"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/query" -Method Post -ContentType "application/json" -Body $body
```
Response:
```
Pod 'nginx-676b6c5bbc-kpftf':
Status: Running
Deployment: nginx
Namespace: default
```

3. Check deployment relationship:
```powershell
$body = @{
    "query" = "Which deployment spawned pod 'nginx-676b6c5bbc-kpftf'"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/query" -Method Post -ContentType "application/json" -Body $body
```
Response:
```
Pod 'nginx-676b6c5bbc-kpftf' was spawned by deployment 'nginx'
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
