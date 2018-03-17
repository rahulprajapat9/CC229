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
### chapter 1
docker --version 
docker info

sudo groupadd docker
sudo usermod -aG docker rp1058 

docker run hello-world
docker image ls
docker container ls --all
docker container ls -aq
