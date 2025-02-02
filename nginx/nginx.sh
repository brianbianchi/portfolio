#!/bin/sh

apt update
apt upgrade
apt install nginx certbot python3-certbot-nginx

# Firewall
ufw allow 'Nginx Full'
ufw delete allow 'Nginx HTTP'
ufw reload

systemctl enable nginx

# Assumes code directory
cp /code/portfolio/nginx/fintasy.io /etc/nginx/sites-available/fintasy.io
ln -s /etc/nginx/sites-available/fintasy.io /etc/nginx/sites-enabled/

# Test nginx config syntax
nginx -t

systemctl restart nginx

certbot --nginx -d fintasy.io -d www.fintasy.io

systemctl status certbot.timer