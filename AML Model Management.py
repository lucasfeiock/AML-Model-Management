

''' Azure Machine Learning (AML) Services
January 12, 2017 - Azure Machine Learning Workbench with Chris Kahrs
Accounced at Microsoft Ignite in September 2017. AML Workbench is a 
cross-platform client for data wrangling and experiment management.
AML Experimentation service helps increase the rate of experimentation 
with data modeling. AML Model Management service hosts, versions, 
and monitors machine learning models. As of January 2018 these services 
are currently in preview mode.

https://docs.microsoft.com/en-us/azure/machine-learning/preview/release-notes-sprint-3
'''


''' Python
https://www.python.org/
https://pypi.python.org/pypi
The latest release of Python is 3.6.4. Python was created by Guido van Rossum 
and released in 1991. It is named after Monty Python, and is a open source 
general-purpose programming language. Python has a large base library and can 
be used for creating GUI desktop, web, and scientific applications. 
pip is Python Package Index (PyPi) and is the official third-party repository 
for Python software. Python Wheels (.whl) are zip format archives and extend 
the base library. Wheels replace the older archives format of Egg (.egg).
'''


''' Overview
0) Azure Machine Learning Workbench
- 0.1) Azure command line interface (CLI)
- 0.2) Login using Azure CLI
- 0.3) Set account
- 0.4) Create resource group

1) Azure Machine Learning Services 
- 1.1) Create Experimentation service
- 1.2) Create Model Management resource
- 1.3) Setup environment and compute

2) Model Building
- 2.1) Create a workspace and project
- 2.2) Submit an experiment
- 2.3) View run history
- 2.4) Promote and download model

3) Azure Machine Learning Model Management
- 3.1) Register model
- 3.2) Create manifest
- 3.3) Create image
- 3.4) Create web service

4) Local deployment using Docker
- 4.1) Images and containers
- 4.2) Image inspect
- 4.3) Consume service
- 4.4) Model Data Collector 
- 4.5) Storage account
'''

'''
Helpful links
https://docs.microsoft.com/en-us/azure/machine-learning/preview/tutorial-iris-azure-cli
https://docs.microsoft.com/en-us/azure/machine-learning/preview/model-management-service-deploy
https://docs.microsoft.com/en-us/azure/machine-learning/preview/how-to-use-model-data-collection
https://github.com/docker/cli/tree/master/experimental#docker-experimental-features
'''

'''
Lessons learned, troubleshooting, hurdles
Azure resources require lowercase names
Docker needs to have experimental features disabled
Add the AML Workbench Python folder to system environment variables
VS Code extensions, Docker, Python, Tools for AI
-help for Azure CLI commands and reference 
'''


# 0 Azure Machine Learning Workbench
# Install Azure Machine Learning Workbench 
# https://docs.microsoft.com/en-us/azure/machine-learning/preview/quickstart-installation
# Windows installer - https://aka.ms/azureml-wb-msi

# Open Command Line Window from within workbench
# C:\Users\<user name>\AppData\Local\AmlWorkbench\Python
# Make sure the Python PATH and Scripts PATH is added to Environment Variables
# setx PATH "%PATH%;C:\path"

# Setup a deployment environment. This is a one time task.
# https://docs.microsoft.com/en-us/azure/machine-learning/preview/deployment-setup-configuration#environment-setup
az provider register -n Microsoft.MachineLearningCompute
az provider register -n Microsoft.ContainerRegistry
az provider register -n Microsoft.ContainerService

# View the registration status 
az provider show -n Microsoft.MachineLearningCompute -o table
az provider show -n Microsoft.ContainerRegistry -o table
az provider show -n Microsoft.ContainerService -o table


# 0) Azure Machine Learning Workbench

# 0.1) Azure Command Line Interface (CLI)
# https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli
# Azure CLI is optimized for managing Azure resources and building
# automation scripts that work against Azure Resource Manager.

# 0.2) Login using Azure CLI
# Log in to Azure.
# https://aka.ms/devicelogin
$ az login

# Show the current account information.
$ az account show

# List all subscriptions available.
$ az account list -o table

# 0.3) Set Account
# Set the current subscription.
$ az account set -s <subscription id or name>

# 0.4) Create a Resource Group
$ az group create --name <resource group name> --location <supported Azure region>
az group create --name azureML --location eastus2





# 1) Azure Machine Learning Services 
# https://azure.microsoft.com/en-us/services/machine-learning-services/

# Workbench - desktop application and CLI to prepare data, steps, and models
# Experimentation service - prototype and control projects
# Model Mangement - deploy and manage models and consume them via web services
# Visual Studio Code Tools for AI - extensions within VS Code
# AI Toolkit for Azure IoT Edge - deploy and run models on IoT devices
# MMLSpark - Microsoft Machine Learning for Apache Spark

# 1.1) Create Experimentation Service

# $ az ml account experimentation create 
# --name <experimentation account name> 
# --resource-group <resource group name>
az ml account experimentation create --name mldemo00 --resource-group azureML

# Now that an Machine Learning Experimentation has been created 
# retry logging back into Azure Machine Learning Workbench.

# 1.2) Create Model Management resource
# $ az ml account modelmanagement create 
# -n <model management account name> 
# -g <resource group name> 
# -l <supported Azure region>
az ml account modelmanagement create -n mldemo00mgmt -g azureML -l eastus2

# 1.3) Setup Environment and Compute
# https://docs.microsoft.com/en-us/azure/machine-learning/preview/deployment-setup-configuration#local-deployment

# This command will create a local deployment and requires Docker.
 $ az ml env setup -l <supported Azure region> -n <env name>
az ml env setup -l eastus2 -n mldemo00local -g azureML

# Cluster deployment is used for high-scale production scenarios.
# --cluster flag is used to set up an ACS with Kubernetes as the orchestrator.
# This step may take 10-20 minutes.
az ml env setup -l eastus2 -n mldemo00cluster -g azureML --cluster

# Monitor environment creation
az ml env show -g azureML -n mldemo00cluster

# Once setup is complete, set your environment for current context
# Verify the resource has been created successfully
# $ az ml env show -g azureML -n mldemo00local
$ az ml env set -g <resource group name> -n <env name>
az ml env set -g azureML -n mldemo00local





# 2) Model Building
# This project will be using the Iris flower dataset.
# https://github.com/Azure/MachineLearningSamples-Iris
# https://en.wikipedia.org/wiki/Iris_flower_data_set

# 2.1) Create a Workspace and Project
# List the project samples
$ az ml project sample list

# Create a new project from the sample
# $ az ml project create 
# --name [project name]
# --workspace [workspace name]
# --account [experimentation account name]
# --resource-group [resource group name]
# --path [local folder path]
# --template-url [url to sample project]
az ml project create --name demoIris --workspace mldemo00Workspace --account mldemo00 --resource-group azureML --path C:\KiZAN\azureML --template-url https://github.com/Azure/MachineLearningSamples-Iris

# Change Directory to the new folder
cd C:\<Your Folder>\demoIris

# 2.2) Submit an experiment
# Submit the iris_sklearn.py file
az ml experiment submit --run-configuration local iris_sklearn.py

# scikit-learn is a machine learning library in Python.
# http://scikit-learn.org/stable/index.html

# This experiment uses Logistic Regression to predict the Iris Species.
# http://scikit-learn.org/stable/modules/linear_model.html#logistic-regression

# 2.3) View Run History
$ az ml history list -o table

# 2.4) Promote and Download model
# Review the storage blob account for the Experimentation Runs 

# Promote artifacts of a run
# $ az ml history promote 
# --run [run id] 
# --artifact-path [file path to model file] 
# --name [name of the file]
az ml history promote --run ID --artifact-path outputs/model.pkl --name model.pkl

# Download the model file to be operationalized
$ az ml asset download --link-file assets\model.pkl.link -d asset_download

# copy asset_download\model.pkl model.pkl

# Create service_schema.json file
az ml experiment submit --run-configuration local score_iris.py
az ml history promote --run ID --artifact-path outputs/service_schema.json --name service_schema.json
az ml asset download --link-file assets\service_schema.json.link -d asset_download

# copy asset_download\service_schema.json service_schema.json





# 3) Azure Machine Learning Model Management
# https://docs.microsoft.com/en-us/azure/machine-learning/preview/model-management-overview
# Enables management and deployment of machine learning workflows and models.
# Docker images are used to provide flexibility to run in multiple environments.

# Docker - disable experimental-features

# 3.1) Register Model
# Load the model into the Model Management resource

# $ az ml model register 
# --model [path to model file] 
# --name [model name]
az ml model register --model model.pkl --name model000

# 3.2) Create Manifest
# Create a manifest for the Docker image

# $ az ml manifest create 
# --manifest-name [your new manifest name] 
# -f [path to code file] 
# -r [runtime for the image, e.g. spark-py]
# -s [schema file e.g. service_schema.json]
# -c [conda dependencies file for additional python packages]
# --model-id [Id of the model]
az ml manifest create --manifest-name manifest000 -f score_iris.py -r python -s service_schema.json -c aml_config\conda_dependencies.yml --model-id

# 3.3) Create Image
# This step may take a few minutes while Creating image...

# $ az ml image create 
# --image-name [image name] 
# -f [path to code file] 
# -r [runtime for the image, e.g. spark-py]
# -s [schema file e.g. service_schema.json]
# -c [conda dependencies file for additional python packages]
# --manifest-id [Id of the manifest]
az ml image create --image-name image000 -f score_iris.py -r python -s service_schema.json -c aml_config\conda_dependencies.yml --manifest-id

# 3.4) Create Web Service
# This step may take a few minutes to Pull the image and start the container

# $ az ml service create realtime 
# -n [service name] 
# -r [runtime for the image, e.g. spark-py]
# --collect-model-data [Enable model data collection]
# --image-id [Id of the image] 
az ml service create realtime -n service000 -r python --collect-model-data true --image-id 

# Get web service usage information
# $ az ml service usage realtime 
# -i [Id of the service]
az ml service usage realtime -i service000

# Get debug logs by calling
az ml service logs realtime -i service000




# 4) Docker
# https://www.docker.com/what-container#/package_software
# https://kubernetes.io/
# https://docs.microsoft.com/en-us/azure/aks/
$ docker -h

# 4.1) Images and Containers
$ docker images
$ docker container
$ docker ps -a

# 4.2) Image Inspect
$ docker image inspect

# 4.3) Consume Service using CLI
az ml service run realtime -i service000 -d "{\"input_df\": [{\"sepal length\": 3.0, \"petal length\": 1.3, \"petal width\": 0.25, \"sepal width\": 3.6}]}"

# Consume Service using CURL
curl -X POST -H "Content-Type:application/json" --data "{\"input_df\": [{\"petal length\": 1.3, \"petal width\": 0.25, \"sepal length\": 3.0, \"sepal width\": 3.6}]}" http://127.0.0.1:32770/score


# 4.4) Model Data Collector 
# Archive model inputs and predictions from a web service.
# https://docs.microsoft.com/en-us/azure/machine-learning/preview/how-to-use-model-data-collection

# Check environment creation
az ml env show -g azureML -n mldemo00cluster

# Switch the environment to run in cluster mode
$ az ml env set -g azureML -n mldemo00cluster

# Create the service on the cluster
az ml service usage realtime -i service000

# 4.5) Storage account
# Check the storage account for the environment.
# This will be used to find the collected data.
# Navigate to the storage account and open the Blob Service Containers blade.
# Next navigate to the model data.
# It may take up to 10 minutes after the first request.
# https://docs.microsoft.com/en-us/azure/machine-learning/preview/how-to-use-model-data-collection#view-the-collected-data
$ az ml env show -v



# Delete all the resource groups
$ az group delete --name <resource group name>

az group list -o table


# Azure Web App - Python / Flask
# Input values and predict value from 
# model on pre built cluster  
# https://kizanml.azurewebsites.net/

# Azure Function - C# Timer Trigger
# Random values sent to model multiple times
# https://kizanmlfunction.azurewebsites.net/ 


