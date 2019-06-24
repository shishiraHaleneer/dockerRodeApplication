# selfiless-acts


##  Build a acts docker image

```
cd acts
docker build -t acts_docker .
```

## Push Docker Image to Docker hub

```
docker login
enter <docker hub username>
enter <docker hub password>

docker tag acts_docker smthn/acts-docker
docker push smthn/acts-docker
```

## pull a docker image and run container

```
docker pull smth/acts-docker
docker run -idt --name acts-docker-v1  -p 8081:5000 smthn/acts-docker
```

## Verify docker continer
```
open browser and enter as below
http://localhost:8081/api/v1/_health
```
if above url returns 200, then good to go
