# Set up for Web Server via Nginx

## 1. Establish server in Vultr by using the following links with instructions:
- Link to create account in Vultr if not already done: https://www.vultr.com/servers/ubuntu/
- Link to create server: https://medium.com/wolf-crypto/how-to-setup-a-vps-on-vultr-d2811cb43bda

Please note, pricing varies according to needs. For installation testing, choose cheapest pricing.

## 2. If using VSCode, just SSH with root user as:
- root@your.ip.address
- pw for root provided by Vultr during initial purchase and setup of VPS.

## 3. Once logged in via terminal, use the following tutorials to establish:
- Sudo user if not already done: https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu
-  Python upgrade - https://docs.vultr.com/how-to-install-python-and-pip-on-ubuntu-24-04
* Please note, the upgrade is only to ensure environment that is set up has the most up-to-date python and you will require to setup a priority of which python to use on the main system (3.8 for Ubuntu 20.04) via the sudo update-alternatives --config python3.
- Nginx install - https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04. Please note, server blocks is not needed as that will be addressed on the tutorial to be followed after.
- Serve flask application tutorial for plotly application initial setup: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
* After reaching installation of gunicorn flask, you must download github instead of creating files according to tutorial. Follow item 4 instructions.

## 4. Add SSH connection to Github repository and download files into app folder
- Follow the instructions on the following link to create an ssh key within the server to establish connection to github account: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux
- Add server's ssh new key to github: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
- After having established the ssh key in your github profile, run *ssh -vT git@github.com* to establish a github connection. The created public key should be used and a message saying "You've successfully authenticated..." should display.
- Clone this repository by running *git clone git@github.com:gsudice/glowcost_dashboard_final.git*. This will create a separate folder downloading all files.
- Move files inside cloned repository folder to app's folder. Example for cosmicgsu app folder (setup during flask tutorial) and glowcost_dashboard_final folder would be: *cp -a ~/glowcost_dashboard_final/. ~/cosmicgsu/*

## 5. Install necessary libraries and test run app
- *pip install -r requirements.txt*

## 6. Return to flask tutorial
- Allow for port to access site by using *sudo ufw allow 5000*
- Run *python app.py*. This should trigger the localhost to open and display the application.
- Create wsgi.py file using *nano ~/projectname/wsgi.py* as per the tutorial with a slight modification on import statement:
*from myproject import app* -> *from myproject import server as app*
- Configure gunicorn: *gunicorn --bind 0.0.0.0:5000 wsgi:app*
- Access landing page as http://your_server_ip:5000.

