# Kubernetes Manifests

This directory includes all necessary files and configurations to deploy _eidos_ in a Kubernetes environment.

The provided configuration sets up a deployment with 3 replicas of the base _eidos_ instance. To deploy an instance with custom functions, simply modify the base Docker image.

# Disclaimer

These manifests are intended for reference only. You must review and modify these manifests to fit your specific cluster and configuration requirements. Ensure that resource requests and limits, image names, environment variables, and other configurations are appropriately set for your environment.
