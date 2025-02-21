# Step up K8s Web App Setup Guide

This guide assumes the following:
- You've already gone through the <a href="https://github.com/khutchi2/simple_k8s_webapp?tab=readme-ov-file"> Simple K8s Webapp </a>
- Running K8s cluster using Rancher Desktop
- You already have K8s, kubectl, etc. installed

## I. dockerhub Repo
1. Because you've already walked through the simpler version of the app, just setup a new repository for this step-up web app.

## II. Project Structure
Same drill as before, either you can clone this repo, or set it all up yourself.  Because I don't want this README to be a novel, I'm going to skip including all of the file contents here and instead just include a brief description of what each file/component is for.
```
my-web-app/
├── Dockerfile
├── app/
│   ├── main.py
│   └── requirements.txt
└── k8s/
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    ├── nginx-configmap.yaml
    ├── nginx-deployment.yaml
    ├── nginx-service.yaml
    └── sqlite-pvc.yaml
```

### 1. Dockerfile
The Dockerfile is the same as before.  Just a basic Python image to run our Flask app in.


### 2. app
#### main.py
This is a basic Flask app with a REST API and a SQLite database.  There are endpoints for retrieving and adding items.  The database initializes when the app starts.

#### requirements.txt
A file for grabbing the needed dependencies for the app to run.  ```flask``` is obviously needed for the Flask app and ```gunicorn``` is for <insert_explanation>.

### 3. k8s
#### flask-deployment.yaml
This will create a K8s deployment for the Flask app.  It spins up the container defined in the Dockerfile, and defines a port to access the app.  It also connects the container to the persistent volume created in ```sqlite-pvc.yaml```.

#### flask-service.yaml
This creates a K8s service which allows access to the pods running from the flask-deployment.

#### nginx-configmap.yaml
This configures nginx to run as a reverse proxy and forwards requests to the Flask backend.

#### nginx-deployment.yaml
This creates a K8s deployment for the nginx reverse proxy.  The ```nginx-configmap.yaml``` is what configures nginx for this.

#### nginx-service.yaml
This creates a service to requests to get to nginx and acts as a load balancer.

#### sqlite-pvc.yaml
This provisions a persistent volume and allows the pods (specifically the sqlite database created by the flask app) to store data permanently even if the app is spun down.

## III. Deployment Steps
This will all be much the same as before.

1. To build Docker image, from the same directory as the Dockerfile, run:
```bash
docker build -t <username>/<repo-name>:webapp .
```

2. To push the docker image to DockerHub, run:
```bash
docker push <username>/<repo-name>:webapp
```

2. Apply the Kubernetes manifests and kick off spinning up the app by running:
```bash
kubectl apply -f k8s/
```
3. Find the pod name (and check that there haven't been any errors) by running:
```bash
kubectl get pods
```

4. To view the web app you'll first need to forward the port.  This is basically how you open up your cluster to your web browser.  You'll need to run the command below.  From the previous command, you can copy and paste the pod with name prefixed "webapp".  (It will probably look something like: *webapp-6b6c6c5498-h4xcf*.)
```bash
kubectl port-forward pod/<pod-name> 5000:5000
```
5. Open a web browser and enter the following into the URL bar:
```
localhost:5000
```
hopefully you'll see a mostly blank page that says, "Hello from Docker!"