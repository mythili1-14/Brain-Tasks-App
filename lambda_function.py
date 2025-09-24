import os
import subprocess
import json
import zipfile

def handler(event, context):
    try:
        # The input artifact from CodePipeline is passed as an event.
        # It contains a reference to the location of the zipped files.
        # You'll need to know the S3 bucket and key from the CodePipeline event.
        # This is a conceptual example, and you may need to adjust based on your pipeline's event structure.
        s3_bucket = event['CodePipelineJob']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']
        s3_key = event['CodePipelineJob']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']
        
        # Download and extract the artifact
        os.system(f"aws s3 cp s3://{s3_bucket}/{s3_key} /tmp/source.zip")
        with zipfile.ZipFile('/tmp/source.zip', 'r') as zip_ref:
            zip_ref.extractall('/tmp/extracted_files')

        # Download and configure kubectl
        os.system("curl -o /tmp/kubectl https://s3.us-west-2.amazonaws.com/amazon-eks/1.24/2022-09-21/bin/linux/amd64/kubectl")
        os.system("chmod +x /tmp/kubectl")
        os.environ["PATH"] += ":/tmp"

        # Configure kubeconfig for EKS
        cluster_name = os.environ.get("EKS_CLUSTER_NAME")
        aws_region = os.environ.get("AWS_REGION")
        subprocess.run([
            "aws", "eks", "update-kubeconfig",
            "--name", cluster_name,
            "--region", aws_region
        ])

        # Apply Kubernetes deployment and service manifests
        # The manifest files are now available in the extracted directory
        subprocess.run(["kubectl", "apply", "-f", "/tmp/extracted_files/kubernetes/deployment.yaml"])
        subprocess.run(["kubectl", "apply", "-f", "/tmp/extracted_files/kubernetes/service.yaml"])
        
        # Wait for the rollout to complete
        subprocess.run([
            "kubectl", "rollout", "status",
            "deployment/brain-tasks-deployment",
            "--namespace", "default"
        ])

        return {"statusCode": 200, "body": "Deployment successful"}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": "Deployment failed"}
