build:
  docker context use default
  docker build -t $REGISTRY/fastapi-demo:latest .

push:
  just build
  docker push $REGISTRY/fastapi-demo:latest
