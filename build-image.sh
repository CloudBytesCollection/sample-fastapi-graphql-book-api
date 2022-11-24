# Builds and Tags Docker Image

# Check platform type (Intel vs Apple chip) -- needed for Heroku and AWS ECS
CHIP_TYPE=`sysctl -n machdep.cpu.brand_string`
IMAGE_NAME=bookapi # use whatever tag you'd like for this (e.g. reponame/bookapi, reponame/customname)

# Modify the following for other chipsets as needed
if [ "$CHIP_TYPE" = "Apple M1 Max" ]; then
  echo "Found Apple chip, building with linux/amd64 platform"
  docker buildx build --platform linux/amd64 -t $IMAGE_NAME -f Dockerfile .
else
  echo "No Apple chip found, build with defaults"
  docker build -t $IMAGE_NAME -f Dockerfile .
fi

echo "Build complete"
docker images $IMAGE_NAME