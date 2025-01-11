# use a python container as a starting point
FROM python:3.7-slim

# install dependencies of interest
RUN python -m pip install rasa

# set workdir and copy data files from disk
# note the latter command uses .dockerignore
WORKDIR /app
#ENV HOME=/rasa
COPY . .

# train a new rasa model
RUN rasa train nlu

# set the user to run, don't run as root
USER 1001

ENTRYPOINT ["rasa"]

CMD ["run","--enable-api","--port","8080"]

