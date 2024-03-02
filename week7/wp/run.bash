#!/bin/bash
docker build -f Dockerfile -t wordpress . && docker run -tip 81:80  wordpress