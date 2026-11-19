#!/usr/bin/env bash
# ==============================================================================
# Kubernetes Deployment & Scaling Demonstration Script
# Component 2 Step 3 & Step 4: Scale from 3 -> 5 -> 3 Replicas
# ==============================================================================

set -e

echo "=== [1/5] Applying Kubernetes ConfigMap ==="
kubectl apply -f configmap.yaml

echo "=== [2/5] Deploying Todo API Application (Initial: 3 Replicas) ==="
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

echo "Waiting for pods to be Ready..."
kubectl rollout status deployment/todo-api-deployment --timeout=60s

echo "=== [3/5] Inspecting Initial 3 Replicas ==="
kubectl get pods -l app=todo-api -o wide
kubectl get svc todo-api-service

echo "=== [4/5] Step 4 Scaling Demo: Scaling Up to 5 Replicas ==="
kubectl scale deployment todo-api-deployment --replicas=5
echo "Waiting for 5 replicas to stabilize..."
kubectl rollout status deployment/todo-api-deployment --timeout=60s
kubectl get pods -l app=todo-api -o wide

echo "=== [5/5] Step 4 Scaling Demo: Scaling Back Down to 3 Replicas ==="
kubectl scale deployment todo-api-deployment --replicas=3
echo "Waiting for scale down to complete..."
kubectl rollout status deployment/todo-api-deployment --timeout=60s
kubectl get pods -l app=todo-api -o wide

echo "Scaling demonstration completed successfully!"
