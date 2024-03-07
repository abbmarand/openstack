#!/bin/bash

command=$1
arg1=$2
arg2=$3

if [ "$command" == "deploy" ]; then
    if [ $arg1 ]; then
        if [ $arg2 ]; then
            echo "Creating stack named: $arg1 on port $arg2"
            db_container_name="${arg1}_db"
            wordpress_container_name="${arg1}_wordpress"
            db_volume_name="db_data_${arg1}"

            docker volume create $db_volume_name

            docker network create $arg1
            docker run -d \
                --name $db_container_name \
                --network $arg1 \
                -e MYSQL_DATABASE=wp \
                -e MYSQL_USER=wp \
                -e MYSQL_PASSWORD=secret \
                -e MYSQL_RANDOM_ROOT_PASSWORD=1 \
                -v $db_volume_name:/var/lib/mysql \
                mysql:8.0

            sleep 10
            db_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${arg1}_db)
            echo $db_ip
            docker run -d \
            --name $wordpress_container_name \
            --network $arg1 \
            -p $arg2:80 \
            -e WORDPRESS_DB_HOST=$db_container_name \
            -e WORDPRESS_DB_NAME=wp \
            -e WORDPRESS_DB_USER=wp \
            -e WORDPRESS_DB_PASSWORD=secret \
            -v $db_volume_name:/var/lib/wordpress \
            wordpress:latest
            
        else
            echo "No port provided"
        fi
    else
        echo "No name provided"
    fi

elif [ "$command" == "destroy" ]; then
    if [ $arg1 ]; then
        echo "Destroying stack with name $arg1"
        db_container_name="${arg1}_db"
        wordpress_container_name="${arg1}_wordpress"
        db_volume_name="db_data_${arg1}"

        docker stop $wordpress_container_name $db_container_name
        docker rm $wordpress_container_name $db_container_name
        docker network rm $arg1
        #docker volume rm $db_volume_name
    else
        echo "No name provided for destroy"
    fi
else
    echo "Unknown command: $command"
    echo "The available commands are deploy and destroy"
fi
