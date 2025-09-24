#!/bin/bash

# Apply Kubernetes deployment and service
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Wait for the deployment to be ready
kubectl rollout status deployment/brain-tasks-deployment --namespace default
