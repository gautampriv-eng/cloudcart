#!/usr/bin/env bash
# ==============================================================================
# Kubernetes Deployment Rollback Demonstration Script
# Component 2 Step 5 Enhancement: Automated Rollback on Failed Deployment
# ==============================================================================

set -e

echo "=== [1/4] Current Revision and Pod State (Healthy Version) ==="
kubectl rollout history deployment/todo-api-deployment
kubectl get pods -l app=todo-api

echo "=== [2/4] Triggering Broken Deployment (Simulating Bad Image Tag) ==="
kubectl set image deployment/todo-api-deployment todo-api=todo-api:invalid-broken-tag --record || true

echo "Observing Pod status during broken deployment..."
sleep 5
kubectl get pods -l app=todo-api

echo "Checking Rollout Status (Failed / Blocked by readiness/liveness)..."
kubectl rollout status deployment/todo-api-deployment --timeout=15s || echo "Rollout blocked as expected!"

echo "=== [3/4] Executing Kubernetes Rollback (kubectl rollout undo) ==="
kubectl rollout undo deployment/todo-api-deployment

echo "Waiting for Rollback to complete..."
kubectl rollout status deployment/todo-api-deployment --timeout=60s

echo "=== [4/4] Verification of Recovered Application State ==="
kubectl rollout history deployment/todo-api-deployment
kubectl get pods -l app=todo-api
echo "Rollback demonstration completed successfully! Service recovered without downtime."
