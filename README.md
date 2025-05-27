# 🚀 HelloWorld AKS + MySQL Deployment

This project demonstrates how to deploy a simple HelloWorld application on **Azure Kubernetes Service (AKS)** using a lightweight virtual machine size and a **Flexible MySQL Server**. It includes database setup, secret management, and Helm deployment.

---

## ✅ Prerequisites

- Azure CLI
- Docker
- kubectl
- Helm
- MySQL client
- A valid Azure account

---

## 🔧 1. Create AKS Cluster

Use the smallest supported VM SKU for AKS system node pools: `Standard_B2s`.

```bash
az aks create \
  --resource-group HelloWorld \
  --name HelloWorld \
  --node-count 1 \
  --node-vm-size Standard_B2s \
  --generate-ssh-keys
```

Get credentials:

```bash
az aks get-credentials --resource-group HelloWorld --name HelloWorld
kubectl get nodes
```

---

## 🛠️ 2. Set Up MySQL Flexible Server

```bash
az mysql flexible-server create \
  --resource-group HelloWorld \
  --name helloworddev123 \
  --location centralus \
  --admin-user helloworld \
  --admin-password 'dDWioih2d54wqwq3' \
  --sku-name Standard_B1s \
  --tier Burstable \
  --version 8.0 \
  --storage-size 20 \
  --public-access 0.0.0.0
```

Connect to it:

```bash
mysql -h helloworddev123.mysql.database.azure.com -u helloworld -p
```

Run SQL:

```sql
CREATE DATABASE helloword;
USE helloword;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO Users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');

SELECT * FROM Users;
```

---

## 🔐 3. Create Kubernetes Secrets

Optionally base64 encode values for Helm:

```bash
echo -n 'helloworddev123.mysql.database.azure.com' | base64
echo -n 'helloword' | base64
echo -n 'helloworld' | base64
echo -n 'dDWioih2d54wqwq3' | base64
```

---

## 📦 4. Deploy with Helm

```bash
helm install helloworld ./helloworld-chart
```

Check resources:

```bash
kubectl get pods
kubectl get svc
```

Example output:

```
helloworld-service   LoadBalancer   <CLUSTER-IP>   <EXTERNAL-IP>   80:PORT/TCP   AGE
```

---

## 🌐 5. Test the App

Replace `<EXTERNAL-IP>`:

```bash
curl http://<EXTERNAL-IP>/health
```

```json
{"status": "healthy"}
```

```bash
curl http://<EXTERNAL-IP>/users
```

Expected output:

```json
[
  {"id":1,"name":"Alice","email":"alice@example.com"},
  {"id":2,"name":"Bob","email":"bob@example.com"}
]
```

---

## 🧪 6. Run the App Locally (Optional)

### Option A: Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

---

### Option B: Docker

```bash
docker build -t helloworld:local .
docker run -p 5000:5000 helloworld:local
```

---

### Option C: Local Kubernetes with Minikube

```bash
minikube start
eval $(minikube docker-env)
docker build -t helloworld:local .
kubectl apply -f k8s/
minikube service helloworld-service
```

---

## 🧹 7. Cleanup

```bash
helm uninstall helloworld
kubectl delete namespace helloworld
```

---

## 📌 Notes

- Use Azure Key Vault for managing secrets in production.
- AKS minimum node VM size is `Standard_B2s`.
- MySQL public access should be restricted in production environments.

---

Happy Deploying! 🚀
