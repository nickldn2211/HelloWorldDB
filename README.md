
# 🚀 HelloWorld AKS + MySQL Deployment

This project demonstrates how to deploy a simple HelloWorld application on **Azure Kubernetes Service (AKS)** using a lightweight virtual machine size and a **Flexible MySQL Server**. It includes database setup, secret management, and Helm deployment.

---

## ✅ Prerequisites

- Azure CLI
- kubectl
- Helm
- MySQL client
- A valid Azure account

---

## 🔧 1. Create AKS Cluster

Use the smallest supported VM SKU for AKS system node pools: `Standard_B2s` (2 vCPUs, 4GB RAM).

```bash
az aks create \
  --resource-group HelloWorld \
  --name HelloWorld \
  --node-count 1 \
  --node-vm-size Standard_B2s \
  --generate-ssh-keys
```

Get cluster credentials:

```bash
az aks get-credentials --resource-group HelloWorld --name HelloWorld
kubectl config current-context
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

Connect to the server:

```bash
mysql -h helloworddev123.mysql.database.azure.com -u helloworld -p
```

Then run the following SQL:

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

## 🔐 3. Create Kubernetes Secret for DB



Optional: Base64-encode values (for Helm chart values):

```bash
echo -n 'helloworddev123.mysql.database.azure.com' | base64
echo -n 'helloword' | base64
echo -n 'helloworld' | base64
echo -n 'dDWioih2d54wqwq3' | base64
```

---

## 📦 4. Deploy with Helm

Install the chart:

```bash
helm install helloworld ./helloworld-chart
```

Check resources:

```bash
helm list -n helloworld
kubectl get pods -n helloworld
kubectl get svc -n helloworld
```

Example output:

```
helloworld-service   LoadBalancer   <CLUSTER-IP>   <EXTERNAL-IP>   80:PORT/TCP   AGE
```

---

## 🌐 5. Test the App

Replace `<EXTERNAL-IP>` with the value from the previous step.

**Health Check:**

```bash
curl http://<EXTERNAL-IP>/health
```

Expected response:

```json
{"status": "healthy"}
```

**Users Endpoint:**

```bash
curl http://<EXTERNAL-IP>/users
```

Expected response:

```json
[
  {"id":1,"name":"Alice","email":"alice@example.com"},
  {"id":2,"name":"Bob","email":"bob@example.com"}
]
```

---

## 🧹 6. Cleanup

Check logs (optional):

```bash
kubectl logs -n helloworld deploy/helloworld-deployment
```

Uninstall everything:

```bash
helm uninstall helloworld -n helloworld
kubectl delete namespace helloworld
```

---

## 📌 Notes

- `Standard_B2s` is the minimum VM size allowed for system node pools in AKS.
- Avoid using hardcoded secrets in production—use Azure Key Vault or secret managers.
- Consider locking down public access to MySQL with VNet rules.

---

Happy Deploying! 🚀
