sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev nginx

sudo -H pip3 install --upgrade pip
    or
sudo apt install python3-pip


sudo -H pip3 install virtualenv
     or
sudo apt install python3-virtualenv


git clone https://github.com/ParitoshBarman/chemiboost.git
cd chemiboost



virtualenv venv
source venv/bin/activate

sudo ufw allow 8000

for test ==> python manage.py runserver 0.0.0.0:8000

pip install django gunicorn


gunicorn --bind 0.0.0.0:8000 aaso.wsgi


deactivate





sudo vim /etc/systemd/system/gunicorn.socket
+++++++++++++++++++++++++++++++++++++++++++++++++
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
+++++++++++++++++++++++++++++++++++++++++++++++++++






sudo vim /etc/systemd/system/gunicorn.service
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/chemiboost
ExecStart=/home/ubuntu/chemiboost/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          aaso.wsgi:application
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




sudo systemctl start gunicorn
sudo systemctl enable gunicorn


sudo systemctl status gunicorn


sudo journalctl -u gunicorn

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

------------------very importent--------------------------------------
curl --unix-socket /run/gunicorn.sock localhost








sudo systemctl daemon-reload
sudo systemctl restart gunicorn





sudo vim /etc/nginx/sites-available/chemiboost
++++++++++++++++++++++++++++++++++++++++++++++++++++
server {
    listen 80 default_server;
    server_name 13.233.190.141;
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
---------------- if want static file css admin------------------------
location /static/ {
        root /home/ubuntu/gb;
    }
-------------------then add this-------------------------------------



------- importent --------
go this ===>> /etc/nginx/sites-available
then delete the defult site by  ==>> sudo rm defultfilename
------- same with ------
/etc/nginx/sites-enabled  ==>> this path







sudo ln -s /etc/nginx/sites-available/chemiboost /etc/nginx/sites-enabled

sudo nginx -t


sudo systemctl restart gunicorn
sudo systemctl restart nginx


sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'


-------*********** For Https *********---------
sudo apt install certbot python3-certbot-nginx

sudo ufw status
sudo ufw allow 'Nginx Full'

if I want multiple domain https  ==>> sudo certbot --nginx -d goobusines.com -d goobusiness.autoimg.xyz
sudo certbot --nginx -d goobusines.com
sudo certbot --nginx -d goo-business.com
sudo certbot --nginx -d indiacreditsales.com
or

sudo certbot --nginx

sudo systemctl restart nginx






for auto renew************
sudo systemctl status certbot.timer


*******For dry run testing********
sudo certbot renew --dry-run











sudo systemctl restart gunicorn
sudo systemctl restart nginx


sudo reboot