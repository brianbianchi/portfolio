#!/bin/sh

if [ "$DEBUG" = "True" ]; then
    echo "Nginx is disabled"
else
    nginx -g "daemon off;"
fi