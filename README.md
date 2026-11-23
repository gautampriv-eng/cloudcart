# CloudCart: End-to-End DevOps CI/CD Pipeline & Kubernetes Deployment

**Course:** DevOps (24CIAEC59)  
**Student:** Gautam Rajesh | **USN:** 1MS24CI045  
**Department:** Computer Science & Engineering (Artificial Intelligence and Machine Learning)  
**Institution:** M. S. Ramaiah Institute of Technology, Bangalore  

---

## 1. Project Overview

This repository contains the complete implementation of the DevOps Course Project for **CloudCart**, an enterprise e-commerce inventory and order management REST microservice developed in Java 17 and Spring Boot 3.3.5.

The project demonstrates a production-grade DevOps lifecycle:
1. **Source Code Management:** Git repository with dual feature branches (`feature/info-endpoint`, `feature/devops`) integrated into `main` via `--no-ff` merge commits.
2. **Build & Dependency Automation:** Apache Maven managing compilation, JUnit 5 MockMvc test suites, and executable fat JAR packaging (`target/cloudcart.jar`).
3. **Continuous Integration (CI):** Declarative Jenkins pipeline with automatic SCM polling (`pollSCM('H/2 * * * *')`), JUnit XML reporting, artifact archiving, and dynamic Docker image tagging (`${IMAGE}:${BUILD_NUMBER}-${GIT_SHA}`). Redundant GitHub Actions workflow (`.github/workflows/ci.yml`).
4. **Configuration Management:** Ansible 2.16 role (`roles/cloudcart`) managing idempotent package installation, dedicated system users, systemd unit templates with dynamic port overrides (`-e app_port=9090`), and handlers.
5. **Containerization:** Multi-stage Dockerfile (`maven:3.9` build stage $\rightarrow$ minimal `eclipse-temurin:17-jre` runtime stage).
6. **Container Orchestration (Kubernetes):** Minikube cluster running a 3-replica Deployment with readiness and liveness health probes, externalized ConfigMap, NodePort Service (port 30080), horizontal replica scaling (3 $\rightarrow$ 5 $\rightarrow$ 3), and zero-downtime rollback recovery.

---

## 2. Repository Layout

```
.
├── src/                          # Spring Boot application source and test code
│   ├── main/java/com/rit/cloudcart/
│   │   ├── CloudCartApplication.java
│   │   ├── controller/           # Product, Order, Info, Health REST controllers
│   │   └── model/                # Product and Order domain models
│   └── main/resources/application.properties
├── pom.xml                       # Maven build and dependency definition
├── Dockerfile                    # Production multi-stage Docker build
├── Jenkinsfile                   # Declarative CI pipeline definition
├── .github/workflows/ci.yml      # GitHub Actions CI workflow
├── ansible/                      # Ansible automation suite
│   ├── inventory                 # Local inventory target
│   ├── playbook.yml              # Main playbook invoking cloudcart role
│   └── roles/cloudcart/          # Defaults, tasks, handlers, templates
├── k8s/                          # Kubernetes resource manifests
│   ├── configmap.yaml            # Externalized configuration
│   ├── deployment.yaml           # 3-replica deployment with health probes
│   └── service.yaml              # NodePort service (port 30080)
├── report/                       # Course project report assets
│   ├── main.tex                  # 23-page Overleaf LaTeX source
│   ├── ramaiah_logo.jpg          # Official institution crest
│   └── screenshots/              # 17 authentic Ubuntu terminal logs
├── DevOps_Course_Project_Report_1MS24CI045.pdf  # Compiled 23-page academic report
└── CI_devops_report_completed.zip               # Overleaf upload package
```

---

## 3. Quick Start & Execution

### Local Build & Test
```bash
mvn clean package
java -jar target/cloudcart.jar --server.port=9091
curl http://localhost:9091/health
curl http://localhost:9091/api/products
```

### Ansible Host Configuration
```bash
cd ansible
ansible-playbook -i inventory playbook.yml -K -e app_port=9090
curl http://localhost:9090/health
```

### Docker Multi-Stage Build & Run
```bash
docker build -t cloudcart:1.0 .
docker run -d -p 8080:8080 cloudcart:1.0
curl http://localhost:8080/health
```

### Kubernetes Minikube Deployment
```bash
minikube start --driver=docker --memory=1900mb --cpus=2 --cni=bridge
minikube image load cloudcart:1.0
kubectl apply -f k8s/
kubectl get deployments,services,pods -o wide

# Scale deployment
kubectl scale deployment cloudcart --replicas=5
kubectl scale deployment cloudcart --replicas=3
```
