# How to daemonize a process
During the creation of the dongle Leo taught me how to daemonize a process. This is a very simple version of it which does not deal with any signal processing like SIGHUP or SIGTERM because the dongle did not need any of that.</br>

Before doing this make sure you have a script or program that you are happy with and can run properly, i.e. is able to run as a process in the foreground.</br>

## Creating a service
To start, we need to create a service file for this program. This can be done by copying this basic template:
```
[Unit]
Description=A description
After=service1.service
Requires=service2.service

[Service]
Restart=on-failure
RestartSec=1
ExecStart=/path/to/your/program

[Install]
WantedBy=multi-user.target
```
into */lib/systemd/system/my.service*.</br>
* Description: Just a description of what the service does
* After: Start this service after service1.service has run
* Requires: This service requires service2.service to be running in order to work
* Restart: When should systemd restart this service restart
* RestartSec: How long should systemd wait after restarting to run the service
* ExecStart: The path to the **executable** program
* WantedBy: Which users should have access to this service</br>

Now run ```systemctl daemon-reload``` to put your new daemon under systemd's radar. There you go, your program is now a daemon.
> NOTE: Whenever you change the *my.service* file, you'll have to run the reload command again

## Monitoring your daemon
To start your service just type ```systemctl start my.service``` and then ```systemctl status my.service``` to see it running. You can also run *stop* and *restart*.</br>

 If there are any output lines of text that come from this file (eg. print statements) they will be captured by journalctl. To see them, type ```journalctl -fu service``` to see the most recent lines of output
