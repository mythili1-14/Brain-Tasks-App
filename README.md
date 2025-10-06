# Brain-Tasks-App CI/CD Pipeline on AWS EKS

This project showcases a complete Continuous Integration and Continuous Deployment (CI/CD) pipeline for a React application, `Brain-Tasks-App`. It uses a custom deployment solution with **AWS Lambda** to deploy to an **AWS EKS** cluster, orchestrated by **AWS CodePipeline**.

## Project Overview

The goal of this project is to automate the deployment of a simple React application to a production-ready Kubernetes cluster. The pipeline is triggered automatically on every commit to the main branch of this GitHub repository. The application runs as a Kubernetes pod and is exposed via an AWS Load Balancer.

## CI/CD Pipeline Explanation

The entire process is orchestrated by **AWS CodePipeline**, which integrates three stages:

  * **Source**: The pipeline is triggered by a commit to this **GitHub repository**. CodePipeline retrieves the source code and passes it to the next stage.
  * **Build**: **AWS CodeBuild** builds the Docker image of the React application as defined in `buildspec.yml`. It then pushes the image to **Amazon ECR** and creates a deployment artifact containing the Kubernetes manifest files (`deployment.yml`, `service.yml`) and the image definition.
  * **Deploy**: This stage uses a **custom AWS Lambda function** to deploy the application. The function is invoked by CodePipeline and its code is responsible for:
      * Retrieving the build artifacts from the CodePipeline S3 bucket.
      * Authenticating with the EKS cluster.
      * Running `kubectl apply -f` commands to deploy the new application version.
      * Reporting the success or failure of the deployment back to CodePipeline.

This approach demonstrates a highly customized and serverless deployment strategy.

-----

## Setup Instructions

1.  **Clone the Repository**:
2.  **AWS ECR**: Create an ECR repository to store the Docker images.
3.  **AWS EKS**: Set up an EKS cluster. Ensure the IAM role for your worker nodes has permissions to create AWS Load Balancers. The EKS cluster must also be configured to allow access from your Lambda function.
4.  **AWS CodeBuild**: Create a CodeBuild project.
5.  **AWS Lambda**: Create a Lambda function for deployment.
6.  **AWS CodePipeline**: Create the pipeline.
