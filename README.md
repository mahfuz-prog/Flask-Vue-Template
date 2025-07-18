# Flask, Vue.js template

### Flask Backend (`flaskapp/`)

* `app.py`: Main Flask application instance creation and extension initialization.

* `config.py`: Centralized configuration management for the Flask app, database, and email settings.

* `users/`: Blueprint for user authentication and management (`/api-v1/users/`).

* `main/`: Blueprint for general application routes or public endpoints (`/api-v1/main/`).

* `notes/`: Blueprint for note creation, retrieval, updating, and deletion (`/api-v1/notes/`).

### Vue.js Frontend (`src`)

* `assets/`: Static assets like CSS.

* `views/`: Vue components representing different pages/views of the application.

* `main.js`: Vue.js application entry point, mounting the root component and configuring Axios, Vue Router, and the store.

* `components/`: Reusable Vue components. Different pages are separated into folders within this directory.

* `utils/`: JavaScript helper functions.

* `router/`: Routes definitions for client-side navigation.

* `store/`: Reactive object for simple state management.


# Server Configuration
### Nginx configuration

```sh
sudo apt install nginx

sudo rm /etc/nginx/sites-enabled/default

nano /etc/nginx/nginx.conf
user username
```

### enable site without ssl

```sh
sudo nano /etc/nginx/sites-enabled/test

server {
  server_name 34.123.176.182;

  include /etc/nginx/proxy_params;

  location / {
    root /home/user/server/frontend/dist;
    try_files $uri /index.html;
  }

  location /api-v1 {
    proxy_pass http://localhost:8000;
  }
}
```

### install ssl

```sh
sudo apt install certbot
sudo apt install software-properties-common
sudo apt install python3-certbot-nginx

sudo certbot --nginx
sudo systemctl restart nginx
```

### after enable ssl nginx server config will look like

```sh
server {
  server_name domain.com www.domain.com;
  root /home/user/test/fontend/dist;
  location / {
    try_files $uri /index.html;
    include /etc/nginx/proxy_params;
    proxy_redirect off;
  }

  location /api {
    proxy_pass http://localhost:8000;
  }

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.domain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = domain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

  listen 80;
  listen [::]:80;
  server_name domain.com www.domain.com;
    return 404; # managed by Certbot
}
```

### firewall
on google cloud only allow https, ssh from firewall settings

```sh
sudo ufw reset
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow https
sudo ufw enable
```

### run flaskapp - Supervisor process manager

```sh
# install supervisor
sudo apt install supervisor

# create supervisor config file
sudo nano /etc/supervisor/conf.d/flaskapp.conf

[program:flaskapp]
directory=/home/username/test/backend
command=/home/username/test/backend/.env/bin/gunicorn -w 5 run:app
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/test/test.err.log
stdout_logfile=/var/log/test/test.out.log
```

### create logfile

```sh
sudo mkdir -p /var/log/test/
sudo touch /var/log/test/test.err.log
sudo touch /var/log/test/test.out.log
```

### Run flask server
```sh
sudo supervisorctl reload		# start running the application
sudo supervisorctl status		# check the status of supervisor
```