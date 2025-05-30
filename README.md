# Server Configuration
### Nginx configuration
change ww-data to username

```sh
sudo apt install nginx
nano /etc/nginx/nginx.conf
user username
```

### enable site without ssl

```sh
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/test

server {
  listen 80;
  listen [::]:80;

  root /home/username/test/fontend/dist;

  location / {
    try_files $uri /index.html;
    include /etc/nginx/proxy_params;
    proxy_redirect off;
  }

  location /api {
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