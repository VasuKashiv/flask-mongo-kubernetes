# Flask and MongoDB Kubernetes Deployment

### 1. How to Build and Push the Docker Image to a Container Registry

1. **Build the Docker Image:**
   ```bash
   docker build -t <your_docker_username>/flask-mongo-app:latest .
2. **Push the docker image to Dockerhub**
   ```bash
   docker push <your_docker_username>/flask-mongo-app:latest
   
### 2. Steps to Deploy the Flask Application and MongoDB on Minikube Kubernetes Cluster

1. **Start Minikube**
   ```bash
   minikube start
2. **Apply MongoDB Secret**
   ```bash
   kubectl apply -f mongo-secret.yaml
3. **Deploy MongoDB StatefulSet and Service:**
   ```bash
   kubectl apply -f mongodb-statefulset.yaml
   kubectl apply -f mongodb-service.yaml
4. **Deploy Flask Application and Service:**
   ```bash
   kubectl apply -f flask-app-deployment.yaml
   kubectl apply -f flask-app-service.yaml
5. **Deploy Horizontal Pod Autoscaler:**
   ```bash
   kubectl apply -f hpa.yaml
6. **Expose Flask Service:**
   To access the Flask application, get the Minikube service URL:
   ```bash
    minikube service flask-app-service

### 3. Explanation of DNS Resolution in Kubernetes
DNS resolution in Kubernetes is handled by an internal DNS service provided by CoreDNS. Each service in Kubernetes gets a DNS name, which allows other pods to communicate with it using this DNS name rather than IP addresses.

Example: The Flask application can connect to MongoDB using the DNS name mongodb-service, which resolves to the cluster IP of the MongoDB service.

DNS resolution works by configuring each pod's /etc/resolv.conf to point to the cluster's DNS service. This allows inter-pod communication to happen seamlessly using service names.

### 4. Explanation of Resource Requests and Limits in Kubernetes
Kubernetes allows you to specify resource requests and limits for each container in a pod. Resource requests guarantee a certain amount of resources (e.g., CPU and memory) for the container, while limits define the maximum amount of resources the container can use.

**Use Case:**

**Requests:** Ensures that a pod has the minimum resources it needs to function.

**Limits:** Prevents a pod from using more resources than it should, avoiding resource contention and ensuring stability.

### 5. Design Choices

**StatefulSet for MongoDB:** Used because MongoDB needs persistent storage and identity stability across restarts.

**Deployment for Flask:** Chosen because Flask is stateless, and using a Deployment ensures ease of scaling and updating.

**NodePort Service for Flask:** Allows external access to the Flask application from the local machine, making it accessible via minikube service.

**PVC and PV for MongoDB:** Ensures data persistence across pod restarts, crucial for a database.

### 6. Testing Scenarios

**Autoscaling Testing:** Simulate high traffic using tools like Apache Bench or Siege to generate requests. Monitor how the Horizontal Pod Autoscaler (HPA) reacts by scaling up the number of Flask pods.

**Database Interaction Testing:** Perform CRUD operations via Flask endpoints to ensure that data is correctly inserted and retrieved from MongoDB. Restart MongoDB pods and verify data persistence using the PV and PVC setup.
