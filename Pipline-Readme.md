
# 🚀 CI/CD Pipeline for AKS Deployment using Azure DevOps

This project uses an Azure DevOps pipeline to build a Docker image, push it to Docker Hub, and deploy it to an Azure Kubernetes Service (AKS) cluster using Helm.

---

## 📌 Prerequisites

Before running the pipeline, make sure you have:

- A **Docker Hub** account
- An **Azure DevOps** project
- An existing **AKS Cluster** in Azure

---

## 🛠️ Azure DevOps Setup

### 1. Create a Docker Hub Service Connection

1. Go to your Azure DevOps project
2. Navigate to **Project settings > Service connections**
3. Click **New service connection > Docker Registry**
4. Choose **Docker Hub**
5. Enter your Docker Hub **username** and **access token**
6. Name it: `dockerhub-service-connection`
7. ✅ Check **"Grant access permission to all pipelines"**
8. Save the connection

### 2. Create a Kubernetes Service Connection

1. Go to **Project settings > Service connections**
2. Click **New service connection > Kubernetes**
3. Choose **Azure Resource Manager** or **Service principal**
4. Select your Azure **subscription**, **resource group**, and **AKS cluster**
5. Name it: `aks-service-connection2`
6. ✅ Check **"Grant access permission to all pipelines"**
7. Save the connection

---




## ✅ Final Notes

- The pipeline is triggered on every push to the `main` branch.
- Ensure both service connections (`dockerhub-service-connection`, `aks-service-connection2`) are created and properly linked in Azure DevOps before running the pipeline.

---

Happy Deploying 🚀
