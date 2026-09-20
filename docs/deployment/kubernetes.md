# Kubernetes Deployment

Deploy PaddleOCRaaS to Kubernetes clusters.

## Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Docker image pushed to registry (Docker Hub, ECR, GCR, etc.)
- Persistent volume support

## Deployment Manifest

Save as `k8s-deployment.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: paddleocr

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: paddleocr-pvc
  namespace: paddleocr
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: paddleocraas
  namespace: paddleocr
spec:
  replicas: 2
  selector:
    matchLabels:
      app: paddleocraas
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: paddleocraas
    spec:
      containers:
      - name: paddleocraas
        image: your-registry/paddleocraas:latest
        ports:
        - containerPort: 8000
        env:
        - name: PADDLEOCR_HOST
          value: "0.0.0.0"
        - name: PADDLEOCR_PORT
          value: "8000"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: paddleocr-storage
          mountPath: /app
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
      volumes:
      - name: paddleocr-storage
        persistentVolumeClaim:
          claimName: paddleocr-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: paddleocraas-service
  namespace: paddleocr
spec:
  selector:
    app: paddleocraas
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: paddleocraas-hpa
  namespace: paddleocr
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: paddleocraas
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Deployment Steps

### 1. Push Image to Registry

```bash
# Docker Hub
docker tag paddleocraas:latest yourusername/paddleocraas:latest
docker push yourusername/paddleocraas:latest

# Or your preferred registry (ECR, GCR, etc.)
```

### 2. Update Image in Manifest

Edit `k8s-deployment.yaml`:
```yaml
image: yourusername/paddleocraas:latest
```

### 3. Deploy to Cluster

```bash
# Create namespace and deploy
kubectl apply -f k8s-deployment.yaml

# Watch deployment
kubectl rollout status deployment/paddleocraas -n paddleocr
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n paddleocr

# Check services
kubectl get services -n paddleocr

# Get LoadBalancer IP/hostname
kubectl get service paddleocraas-service -n paddleocr
```

### 5. Access Application

```bash
# Get external IP
EXTERNAL_IP=$(kubectl get service paddleocraas-service -n paddleocr -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Access
echo "Visit: http://$EXTERNAL_IP/static/index.html"
```

## Monitoring

### View Logs

```bash
# View logs from specific pod
kubectl logs -f <pod-name> -n paddleocr

# View logs from all pods
kubectl logs -f deployment/paddleocraas -n paddleocr
```

### Check Resource Usage

```bash
# CPU and memory
kubectl top pods -n paddleocr
kubectl top nodes
```

### Pod Status

```bash
# Describe pod to see events
kubectl describe pod <pod-name> -n paddleocr

# Get pod details
kubectl get pods -n paddleocr -o wide
```

## Scaling

### Manual Scaling

```bash
# Scale to 3 replicas
kubectl scale deployment paddleocraas --replicas=3 -n paddleocr
```

### Automatic Scaling

Configured in HPA section of manifest. Automatically scales based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)

## Troubleshooting

### Pod Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n paddleocr

# Check logs
kubectl logs <pod-name> -n paddleocr
```

### Health Check Failures

```bash
# Manually test health endpoint
kubectl exec <pod-name> -n paddleocr -- curl http://localhost:8000/health
```

### Storage Issues

```bash
# Check PVC status
kubectl get pvc -n paddleocr

# Check PV status
kubectl get pv
```

---

**See Also:** [Production Deployment](production.md)
