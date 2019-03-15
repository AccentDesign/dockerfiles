FROM        nginx:alpine

COPY        nginx.conf /etc/nginx/nginx.conf
COPY        nginx-app.conf /etc/nginx/conf.d/default.conf
COPY        maintenance.html /locust/www/fallback/htdocs/maintenance.html