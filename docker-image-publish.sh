# Publishes an image to Docker hub
# Can be used for either public or private repositories

REPO_NAME=viratecinteractive # replace with your repo name
IMAGE_NAME=bookapi # change this to whatever image name was given in your docker build
TAG_NAME=latest # change this to whatever tag you'd like or make it a pass-in var

# Push up to Docker Hub
docker push $REPO_NAME/$IMAGE_NAME:$TAG_NAME
