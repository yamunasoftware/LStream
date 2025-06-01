#!/bin/bash

docker buildx prune -f
docker compose down
docker compose build
docker compose up -d