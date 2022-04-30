# Deploys the pre-built image to Heroku

# Log into Heroku container registry, tag the image, and push up
APP_NAME=bookapi-dev # change this to your src name

heroku container:login
docker tag bookapi registry.heroku.com/$APP_NAME/web
docker push registry.heroku.com/$APP_NAME/web

# Release (complete deployment)
heroku container:release web --app $APP_NAME
