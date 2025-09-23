#!/bin/bash

# Apply Kubernetes deployment and service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Wait for the deployment to be ready
kubectl rollout status deployment/brain-tasks-deployment --namespace default
