# Docker

## What?
- Lightweight: containers leverage and share the host kernel (very bare OS)
- Scalable: can create the rplicas easily
- Stackable: can stack more containers vertically

## Why?
- Make app portable (from data center to cloud, VM to baremetal, migration from one vendor to another)

## images and containers
- container is launched by running the image (which is an executable package: code, libs, runtime, env variables, config files)

## Getting started
### chapter 1 Intro
- docker --version 
- docker info

- sudo groupadd docker
- sudo usermod -aG docker rp1058 
 
- docker run hello-world
- docker image ls
- docker container ls --all
- docker container ls -aq

### Chapter 2 define a container with DockerFile
- vi Dockerfile
- vi requirements.txt
- vi app.py

- docker build -t friendlyhello .  # Create image using this directory's Dockerfile

- docker run -p 4000:80 friendlyhello  # Run "friendlyname" mapping port 4000 to 80

- docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode

- docker container ls                                # List all running containers
- docker container ls -a             # List all containers, even those not running
- docker container stop <hash>           # Gracefully stop the specified container
- docker container kill <hash>         # Force shutdown of the specified container
- docker container rm <hash>        # Remove specified container from this machine
- docker container rm $(docker container ls -a -q)         # Remove all containers
- docker image rm <image id>            # Remove specified image from this machine
- docker image rm $(docker image ls -a -q)   # Remove all images from this machine

- docker login             # Log in this CLI session using your Docker credentials

- docker tag <image> username/repository:tag  # Tag <image> for upload to registry
 
- docker push username/repository:tag            # Upload tagged image to registry
 
- docker run username/repository:tag                   # Run image from a registry
