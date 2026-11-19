# DevOps End-to-End CI/CD Pipeline & Kubernetes Deployment

**Course Code:** 25CIAEC59 / 25CYAEC59 | **Credits:** 1:0:0  
**Student Name:** Gautam Rajesh | **USN:** 1MS24CI045  
**Department:** Computer Science & Engineering (Artificial Intelligence and Machine Learning)  
**Institution:** Ramaiah Institute of Technology, Bangalore  

---

## 1. Project Overview & Architecture

This repository implements a complete, end-to-end DevOps automation pipeline for an enterprise microservice:
**Code $\rightarrow$ Version Control $\rightarrow$ Continuous Integration (Jenkins & GitHub Actions) $\rightarrow$ Configuration Management (Ansible) $\rightarrow$ Containerization (Docker) $\rightarrow$ Orchestration & Scaling (Kubernetes)**.

```
+------------------------------------------------------------------------------------------------+
|                                    DevOps Assembly Line                                       |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|   +--------------+      +-------------------+      +------------------+      +---------------+ |
|   |  Developer   | ---> |   Git & GitHub    | ---> | Jenkins / Actions| ---> | Build Artifact| |
|   |  Code & Test |      | Feature & Merges  |      | CI Automated Test|      | & Version Tag | |
|   +--------------+      +-------------------+      +------------------+      +---------------+ |
|                                                                                      |         |
|                                                                                      v         |
|   +--------------+      +-------------------+      +------------------+      +---------------+ |
|   |  Kubernetes  | <--- | Multi-Stage Docker| <--- | Ansible Playbook | <--- | Container     | |
|   | Pods & Scale |      | Production Image  |      | Roles & Handlers |      | Packaging     | |
|   +--------------+      +-------------------+      +------------------+      +---------------+ |
+------------------------------------------------------------------------------------------------+
```

---

## 2. Component 1: CI/CD Pipeline with Git, Build Tool & Jenkins (10 Marks)

### Step 1: Application Architecture
- **Language/Framework:** Python 3.12 / Flask REST API
- **In-Memory Store:** `TaskRepository` thread-safe in-memory task management
- **Endpoints:**
  - `GET /` — API metadata, route catalog, author info, operational status
  - `GET /api/todos` — Retrieve all tasks (supports `?completed=true|false`)
  - `POST /api/todos` — Create a new task (`title`, `description`, `priority`)
  - `GET /api/todos/<id>` — Retrieve single task details by ID
  - `PUT /api/todos/<id>` — Update task attributes and completion state
  - `DELETE /api/todos/<id>` — Delete task by ID
  - `GET /health` — Kubernetes liveness and readiness probe endpoint
  - `GET /metrics` — Observability and request metrics endpoint

### Step 2: Version Control & Git History
The repository features feature branching and non-fast-forward merge history:
- Main branch: `main`
- Feature branch: `feature/rest-api-endpoints`
- Merge commit: `Merge branch 'feature/rest-api-endpoints' into main (PR #1: Implement Task REST API & Unit Tests)`

```bash
git log --graph --oneline --all
```

### Step 3: Build & Automated Unit Testing
To run the automated test suite locally:
```bash
pip install -r requirements.txt
pytest -v tests/
```
Output:
```
tests/test_api.py::test_index_endpoint PASSED                            [  9%]
tests/test_api.py::test_health_probe PASSED                              [ 18%]
tests/test_api.py::test_metrics_endpoint PASSED                          [ 27%]
tests/test_api.py::test_list_todos PASSED                                [ 36%]
tests/test_api.py::test_create_todo_success PASSED                       [ 45%]
tests/test_api.py::test_create_todo_validation_empty_title PASSED        [ 54%]
tests/test_api.py::test_create_todo_validation_no_json PASSED            [ 63%]
tests/test_api.py::test_get_todo_by_id PASSED                            [ 72%]
tests/test_api.py::test_get_todo_not_found PASSED                        [ 81%]
tests/test_api.py::test_update_todo PASSED                               [ 90%]
tests/test_api.py::test_delete_todo PASSED                               [100%]
============================= 11 passed in 0.39s ==============================
```

### Step 4 & 5: Jenkins Declarative CI Pipeline & Enhancements
The `Jenkinsfile` configures a declarative CI workflow:
1. **Poll SCM Trigger:** `pollSCM('H/2 * * * *')` automatically monitors Git commits.
2. **Static Code Analysis:** `flake8` linting and syntax compliance.
3. **CI Enhancement 1 (Automated Tests in CI):** Pre-build test execution producing JUnit XML test reports (`reports/test-results.xml`).
4. **CI Enhancement 2 (Commit SHA Versioning):** Artifacts and Docker images tagged dynamically with `${BUILD_NUMBER}-${GIT_COMMIT_SHORT}`.
5. **CI Enhancement 3 (Dual CI / GitHub Actions):** `.github/workflows/ci.yml` runs multi-version Python matrices and builds container images on every push.
6. **Artifact Archival:** Archives compressed packages `dist/*.tar.gz` and test reports for traceability.

---

## 3. Component 2: Configuration Management (Ansible) & Kubernetes Deployment (10 Marks)

### Step 1: Ansible Playbook & Roles
The infrastructure configuration is modularized via Ansible roles:
- **Inventory (`ansible/inventory.ini`):** Defines target host groups and SSH/connection settings.
- **Variables (`ansible/roles/todo_app/defaults/main.yml`):** Reusable settings (`app_port`, `app_user`, `app_dir`, `app_env`).
- **Handlers (`ansible/roles/todo_app/handlers/main.yml`):** `Restart todo-app service` and `Reload systemd daemon` triggered only upon file/template changes.
- **Role Tasks (`ansible/roles/todo_app/tasks/main.yml`):**
  1. Installs system packages (`python3`, `python3-pip`, `python3-venv`, `curl`).
  2. Creates unprivileged system user `devops`.
  3. Prepares deployment directory `/opt/todo-api`.
  4. Deploys code and installs dependencies in an isolated virtual environment.
  5. Renders systemd service unit template (`todo-app.service.j2`).
  6. Enables and starts the service, validating health with an HTTP URI probe.

Execution command:
```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml
```

### Step 2: Containerization (Multi-Stage Dockerfile)
- **Deployment Enhancement:** Multi-stage build separates build tooling from the final runtime image:
  - **Stage 1 (Builder):** Uses `python:3.12-slim` to compile wheels.
  - **Stage 2 (Runtime):** Lightweight image containing only installed wheels, unprivileged `appuser:appgroup` (UID 10001), built-in healthcheck, and Gunicorn WSGI server.
```bash
docker build -t todo-api:latest .
docker run -d -p 5000:5000 --name todo-api-demo todo-api:latest
curl http://localhost:5000/health
```

### Step 3: Kubernetes Deployment & Services
- **ConfigMap (`k8s/configmap.yaml`):** Externalizes configuration parameters (`PORT`, `APP_ENV`, `LOG_LEVEL`).
- **Deployment (`k8s/deployment.yaml`):**
  - Replicas: 3
  - Labels & Selectors: `app: todo-api, tier: backend`
  - Health Probes: `livenessProbe` and `readinessProbe` checking `/health` every 5-10 seconds.
- **Service (`k8s/service.yaml`):** Exposes pods via `NodePort: 30080` (or `ClusterIP`).

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -l app=todo-api
kubectl get svc todo-api-service
```

### Step 4: Kubernetes Scaling Demonstration
Demonstrating scaling from 3 to 5 replicas, and scaling back down:
```bash
# Scale up to 5 replicas
kubectl scale deployment todo-api-deployment --replicas=5
kubectl get pods -l app=todo-api -o wide

# Scale down back to 3 replicas
kubectl scale deployment todo-api-deployment --replicas=3
kubectl get pods -l app=todo-api -o wide
```

### Step 5: Deployment Enhancements
1. **ConfigMap Integration:** Dynamic runtime configuration without modifying container images.
2. **Liveness & Readiness Probes:** Automatic pod restart on application deadlock and traffic blackholing until initialization completes.
3. **Automated Rollback:**
   ```bash
   # Deploy bad image tag
   kubectl set image deployment/todo-api-deployment todo-api=todo-api:invalid-tag
   # Observe rollout failure and rollback
   kubectl rollout undo deployment/todo-api-deployment
   kubectl rollout status deployment/todo-api-deployment
   ```

---

## 4. Verification and Curl Commands

```bash
# 1. Root Information Endpoint
curl -X GET http://localhost:5000/

# 2. Health Check (Probes)
curl -X GET http://localhost:5000/health

# 3. Metrics Telemetry
curl -X GET http://localhost:5000/metrics

# 4. List All Todos
curl -X GET http://localhost:5000/api/todos

# 5. Create New Todo
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Implement Prometheus Alerts","description":"Alert on high container memory","priority":"HIGH"}'

# 6. Update Todo Status
curl -X PUT http://localhost:5000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# 7. Delete Todo
curl -X DELETE http://localhost:5000/api/todos/2
```

---

## 5. Resume Framing (Outcomes Format)

- **Component 1 (CI/CD Pipeline):**  
  *Automated build-and-test CI pipeline using Jenkins declarative pipelines and GitHub Actions triggered on Git push, integrating automated pytest unit testing, code linting, dynamic Git SHA versioning, and automated artifact archival.*
- **Component 2 (Configuration & Kubernetes):**  
  *Configured automated host provisioning with an Ansible role and handlers; containerized the service using a multi-stage Dockerfile and deployed to Kubernetes with ConfigMap configuration, liveness/readiness self-healing probes, zero-downtime scaling, and automated rollback support.*
