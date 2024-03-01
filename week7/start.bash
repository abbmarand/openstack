#!/bin/bash


service php8.1-fpm start
service nginx start
# Keep the container running
exec /bin/bash
