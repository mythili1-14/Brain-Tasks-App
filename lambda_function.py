import os
import subprocess
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        logger.info("Starting Lambda deployment function...")

        # Get environment variables from Lambda configuration
        cluster_name = os.environ.get("EKS_CLUSTER_NAME")
        aws_region = os.environ.get("AWS_REGION")

        # 1. Download and configure kubectl
        logger.info("Downloading and configuring kubectl...")
        subprocess.run(
            ["curl", "-o", "/tmp/kubectl", 
             "https://s3.us-west-2.amazonaws.com/amazon-eks/1.24/2022-09-21/bin/linux/amd64/kubectl"]
        )
        os.chmod("/tmp/kubectl", 0o755)
        os.environ["PATH"] = os.environ["PATH"] + ":/tmp"

        # 2. Configure kubeconfig for EKS cluster access
        logger.info("Configuring kubeconfig...")
        subprocess.run([
            "aws", "eks", "update-kubeconfig",
            "--name", cluster_name,
            "--region", aws_region
        ], check=True)
        
        # 3. Execute the custom deployment script from the artifacts
        logger.info("Executing custom deployment script...")
        subprocess.run(["chmod", "+x", "./scripts/deploy.sh"], check=True)
        subprocess.run(["./scripts/deploy.sh"], check=True)

        logger.info("Deployment successful.")
        return {"statusCode": 200, "body": "Deployment successful"}

    except subprocess.CalledProcessError as e:
        logger.error(f"Deployment failed: {e}")
        return {"statusCode": 500, "body": f"Deployment failed: {e.output}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"statusCode": 500, "body": "An unexpected error occurred"}
