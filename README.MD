# Set up for Web Server via Nginx

1. Establish server in Vultr by using the following links with instructions:
- Link to create account in Vultr if not already done: https://www.vultr.com/servers/ubuntu/
- Link to create server: https://medium.com/wolf-crypto/how-to-setup-a-vps-on-vultr-d2811cb43bda

Please note, pricing varies according to needs. For installation testing, choose cheapest pricing.

2. If using VSCode, just SSH with root user as:
- root@your.ip.address
- pw for root provided by Vultr during initial purchase and setup of VPS.

3. Once logged in via terminal, use the following tutorials to establish:
- Sudo user if not already done: https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu
-  Python upgrade - https://docs.vultr.com/how-to-install-python-and-pip-on-ubuntu-24-04
* Please note, the upgrade is only to ensure environment that is set up has the most up-to-date python and you will require to setup a priority of which python to use on the main system (3.8 for Ubuntu 20.04) via the sudo update-alternatives --config python3.
- Nginx install - https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04
- Serve flask application tutorial for plotly application initial setup: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04
