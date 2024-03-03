FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install nginx php-fpm wget -y


RUN wget -O latest.tar.gz https://wordpress.org/latest.tar.gz
RUN tar -xf latest.tar.gz
RUN rm -rf latest.tar.gz
RUN chown -R www-data:www-data wordpress/
RUN mv wordpress/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html
COPY ./default /etc/nginx/sites-enabled/

RUN apt-get install php-mysql mysql-server mysql-client -y
COPY init.sql /init.sql
COPY --chown=www-data:www-data wp-config.php /var/www/html/wp-config.php

EXPOSE 3306
EXPOSE 80
COPY --chown=root:root start.bash .
RUN chmod +x start.bash
CMD "./start.bash"
