#!/bin/bash
service mysql start && mysql < /init.sql && service mysql restart
service php8.1-fpm start
service nginx start
# Keep the container running
exec /bin/bash
