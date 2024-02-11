#!bin/bash
sudo su
apt update 
apt install nginx php-fpm -y
rm -rf /var/www/html/
wget -O latest.tar.gz https://wordpress.org/latest.tar.gz
tar -xf latest.tar.gz
rm -rf latest.tar.gz
sudo chown -R www-data:www-data wordpress/
mv wordpress/ /var/www/html
echo '
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        root /var/www/html;
        index index.php;
        server_name _;
        location ~ \.php$ {
                include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        }
}
' > /etc/nginx/sites-enabled/default
apt install php-mysql mysql-server mysql-client -y
mysql -e "CREATE DATABASE wp;"
mysql -e "CREATE USER 'wp'@'localhost' IDENTIFIED BY 'secret';"
mysql -e "GRANT ALL PRIVILEGES ON wp.* TO 'wp'@'localhost';"
cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php
chown www-data:www-data /var/www/html/wp-config.php
echo '<?php
define( "DB_NAME", "wp" );
define( "DB_USER", "wp" );
define( "DB_PASSWORD", "secret" );
define( "DB_HOST", "localhost" );
define( "DB_CHARSET", "utf8" );
define( "DB_COLLATE", "" );
define( "AUTH_KEY",         "put your unique phrase here" );
define( "SECURE_AUTH_KEY",  "put your unique phrase here" );
define( "LOGGED_IN_KEY",    "put your unique phrase here" );
define( "NONCE_KEY",        "put your unique phrase here" );
define( "AUTH_SALT",        "put your unique phrase here" );
define( "SECURE_AUTH_SALT", "put your unique phrase here" );
define( "LOGGED_IN_SALT",   "put your unique phrase here" );
define( "NONCE_SALT",       "put your unique phrase here" );
$table_prefix = "wp_";

define( "WP_DEBUG", false );
if ( ! defined( "ABSPATH" ) ) {
        define( "ABSPATH", __DIR__ . "/" );
}
require_once ABSPATH . "wp-settings.php";
' > /var/www/html/wp-config.php
systemctl restart nginx