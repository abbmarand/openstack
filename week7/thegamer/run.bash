#!/bin/bash
docker build -f Dockerfile -t mynginx . && docker run -tip 80:80 mynginx