# Cloud Deployment

Deploy PaddleOCRaaS to major cloud providers.

## AWS ECS

### Prerequisites
- AWS account
- AWS CLI configured
- Docker image pushed to ECR

### Deploy to ECS

```bash
# Create ECR repository
aws ecr create-repository --repository-name paddleocraas

# Build and push image
docker tag paddleocraas:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/paddleocraas:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/paddleocraas:latest

# Create task definition (use AWS console or CLI)
# Configure service in ECS
# Set ALB for load balancing
```

## Google Cloud Run

### Deploy

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/paddleocraas

# Deploy
gcloud run deploy paddleocraas \
  --image gcr.io/PROJECT_ID/paddleocraas \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 3600 \
  --allow-unauthenticated
```

Access at: `https://paddleocraas-<id>.run.app`

## Azure Container Instances

### Deploy

```bash
# Push to ACR
az acr build --registry <registry-name> --image paddleocraas:latest .

# Deploy container
az container create \
  --resource-group <group> \
  --name paddleocraas \
  --image <registry>.azurecr.io/paddleocraas:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --environment-variables \
    PADDLEOCR_HOST=0.0.0.0 \
    PADDLEOCR_PORT=8000
```

---

**See Also:** [Production Deployment](production.md), [Kubernetes Deployment](kubernetes.md)
