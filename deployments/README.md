# Kubernetes deployment of eidos
This folder contains all required files and configuration to have a working deployment of `eidos` in Kubernetes.

The configuration provided creates a deployment with 3 replicas using the base `eidos` instance (to deploy a instance with custom functions just change the docker image) behind a service for load balancing between the different pods.

# Disclaimer

The provided Kubernetes manifests are for reference only. You must review and adjust these manifests to suit your specific cluster and configuration. Ensure that resource requests and limits, image names, environment variables, and other configurations are appropriate for your setup.