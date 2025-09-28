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

This approach demonstrates a highly customized and serverless deployment strategy. .

-----

## Setup Instructions

To set up this project, you must have an AWS account with the necessary permissions.

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/Vennilavan12/Brain-Tasks-App.git
    cd Brain-Tasks-App
    ```

2.  **AWS ECR**: Create an ECR repository to store the Docker images.

3.  **AWS EKS**: Set up an EKS cluster. Ensure the IAM role for your worker nodes has permissions to create AWS Load Balancers. The EKS cluster must also be configured to allow access from your Lambda function.

4.  **AWS CodeBuild**: Create a CodeBuild project.

      * **Source**: Link it to this GitHub repository.
      * **Environment**: Choose a managed image like `Amazon Linux 2`.
      * **Buildspec**: Use the `buildspec.yml` file from the repository to define the Docker build and artifact creation process.
      * **Environment Variables**: Define the following variables: `AWS_ACCOUNT_ID`, `AWS_DEFAULT_REGION`, and `IMAGE_REPO_NAME`.

5.  **AWS Lambda**: Create a Lambda function for deployment.

      * **Runtime**: Python 3.9+ is a good choice.
      * **Code**: The function's code must include logic to retrieve artifacts from CodePipeline's S3 bucket and use a Kubernetes client library (like `kubernetes-py`) to perform the deployment.
      * **IAM Role**: The function's execution role must have permissions for `s3:GetObject` on the CodePipeline artifact bucket, and full administrative access to your EKS cluster (`eks:*`).

6.  **AWS CodePipeline**: Create the pipeline.

      * **Source Stage**: Select `GitHub` and link to this repository.
      * **Build Stage**: Choose the CodeBuild project you created.
      * **Deploy Stage**: Select **AWS Lambda** as the action provider and choose the Lambda function you created. Configure the input artifact to be the output from the "Build" stage.

-----

## Screenshots and Pipeline Status

<img src="https://github.com/mythili1-14/Brain-Tasks-App/blob/main/screenshots/Screenshot_20250925_201016.png" alt="Banner" />
<img src="https://github.com/mythili1-14/Brain-Tasks-App/blob/main/screenshots/Screenshot_20250925_234744.png" alt="Banner" />
<img src="https://github.com/mythili1-14/Brain-Tasks-App/blob/main/screenshots/Screenshot_20250925_203355.png" alt="Banner" />


** More Images available at /screenshots**
-----

## Application Load Balancer ARN

After a successful deployment, the AWS Load Balancer ARN for the application can be found in the EC2 console.

**Load Balancer ARN**: `http://af4f7528d501e4a29a30018ec24074fd-1452852875.us-east-1.elb.amazonaws.com/`
