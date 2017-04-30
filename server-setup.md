Instructions to install a development multi variant fishtest server, tested working with Ubuntu from 15.10 to 17.04.

1. Make a clean install of Ubuntu (virtual machine, cloud instance, lxd etc.)
2. Login to Ubuntu and write this script *setup-fishtest.sh*

  ```bash
  #!/bin/bash
  # to setup a multi variant fishtest server on Ubuntu, simply run: 
  # sudo bash setup-fishtest.sh
  #
  # to use fishtest open a browser and connect to:
  # http://<ip-address>:6543
  
  # install required packages
  apt update
  apt install -y unzip zsh
  apt install -y mongodb-server
  apt install -y python python-dev python-pip python-numpy python-scipy python-zmq
  
  pip install --upgrade pip
  pip install pyramid
  pip install waitress
  pip install boto
  pip install requests
  
  # create user fishtest
  useradd -m fishtest
  
  # download and prepare fishtest
  sudo -i -u fishtest << EOF
  wget https://github.com/ianfab/fishtest/archive/master.zip
  unzip master.zip
  mv fishtest-master fishtest
  touch fishtest.secret
  EOF
  
  # apply a patch to add some default users:
  # "user00" (with password "user00"), as approver
  # "user01" (with password "user01"), as normal user
  
  sudo -i -u fishtest patch -p0 << EOF
  diff -Naur fishtest-master/fishtest/fishtest/__init__.py fishtest/fishtest/fishtest/__init__.py
  --- fishtest-master/fishtest/fishtest/__init__.py	2016-01-03 18:42:35.000000000 +0100
  +++ fishtest/fishtest/fishtest/__init__.py	2016-01-06 22:12:12.404453300 +0100
  @@ -70,4 +70,14 @@
     config.add_route('api_request_spsa', '/api/request_spsa')
   
     config.scan()
  +  
  +  # IMPORTANT: use this code only to initialize a development site
  +  if not rundb.userdb.get_user('user00'):
  +    # add user00 as approver
  +    rundb.userdb.create_user('user00', 'user00', 'user00@user00.user00')     
  +    rundb.userdb.add_user_group('user00', 'group:approvers')
  +    #add user01 as normal user
  +    rundb.userdb.create_user('user01', 'user01','user01@user01.user01')
  +  ###
  +  
     return config.make_wsgi_app()
  EOF
       
  # setup fishtest
  cd /home/fishtest/fishtest/fishtest
  python setup.py develop
  
  # install fishtest as systemd service
  cat << EOF > /etc/systemd/system/fishtest.service
  [Unit]
  Description=Fishtest Server: connect to port 6543
  After=multi-user.target
  
  [Service]
  Type=forking
  ExecStart=/home/fishtest/fishtest/fishtest/start.sh
  Restart=on-failure
  RestartSec=3
  User=fishtest
  WorkingDirectory=/home/fishtest/fishtest/fishtest
  
  [Install]
  WantedBy=graphical.target
  EOF

  # install also fishtest debug as systemd service
  cat << EOF > /etc/systemd/system/fishtest_dbg.service
  [Unit]
  Description=Fishtest Server Debug: connect to port 6542
  After=multi-user.target
    
  [Service]
  Type=simple
  ExecStart=/home/fishtest/fishtest/fishtest/start_dev.sh
  User=fishtest
  WorkingDirectory=/home/fishtest/fishtest/fishtest
  
  [Install]
  WantedBy=graphical.target
  EOF

  # enable the autostart for fishtest.service
  systemctl daemon-reload
  systemctl enable fishtest.service

  # start fishtest server
  systemctl start fishtest.service
  

  ```

3. Run the setup script using sudo

  ```
  sudo -H bash setup-fishtest.sh
  ```

4. Open a web browser using the ip_address of the fishtest server and the port 6543 (http://ip_address:6543/login) and create some tests with these users:
  * user00 (with password user00), to approve test
  * user01 (with password user01), to create test

5. Connect a worker using the ip_address of the fishtest server and the port 6543, to have multiple workers make some copies of *worker* folder.
  ```
  python worker.py --host <ip_address> --port 6543 --concurrency <n_cores> <username> <password>
  ```

6. To debug the server with the Pyramid Debug Toolbar, login on Ubuntu, use the following commands to start/stop the `fishtest_dbg.service`, and open a browser using the port 6542 (http://ip_address:6542).

  ```
  # start the debug session
  sudo systemctl start fishtest_dbg.service
  
  # stop the debug session
  sudo systemctl stop fishtest_dbg.service
  ```
