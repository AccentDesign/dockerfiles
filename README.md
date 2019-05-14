# dockerfiles

example projects and dockerfiles

## accent/nginx-uwsgi

Uses uwsgi_pass and expects a uwsgi protocol to be running on ``app:8000``.
If a ``/ws/`` path is tried it proxies off to ``app:8001`` using proxy_pass.

    docker build -t accent/nginx-uwsgi:latest nginx-uwsgi/

## accent/nginx-proxy

Uses proxy_pass and expects a uwsgi http protocol to be running on ``app:8000``.

    docker build -t accent/nginx-proxy:latest nginx-proxy/

## accent/nginx-proxy-all

Uses proxy_pass and expects a uwsgi http protocol to be running on ``app:8000``.

    docker build -t accent/nginx-proxy-all:latest nginx-proxy-all/
