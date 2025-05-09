#!/bin/sh

apt update
apt upgrade
apt install nginx certbot python3-certbot-nginx

# Firewall
ufw allow 'Nginx Full'
ufw allow 'Nginx HTTPS'
ufw reload

systemctl enable nginx

# Assumes code directory
cp /code/portfolio/nginx/mockfinance.com /etc/nginx/sites-available/mockfinance.com
ln -s /etc/nginx/sites-available/mockfinance.com /etc/nginx/sites-enabled/

# Test nginx config syntax
nginx -t

systemctl restart nginx

certbot --nginx -d mockfinance.com

systemctl status certbot.timer