# Getting familiar with the Cisco ASA
The purpose of this task was to familiarize myself with the ASA (Adaptive Security Appliance) CLI (Command Line Interface) and be comfortable with configuring it.

### Creating the ASAv
Bryan created a dev environment for me to play around in and set-up the ASAv following instructions from [SLVPN/ASAV](https://github.office.opendns.com/slvpn/asav). Once created it's important to note the address and network IPs (139.178.91.146 and 139.178.91.144/29 in this case).</br>
Bryan then ran an Ansible config that set up the dev environment to be like all the other ones in use. Once complete, I used:
```
ssh 139.178.91.146 -L 5901:127.0.0.1:5920 -N
```
to ssh into the asav and used **VNC Viewer** to see the monitor. From there I could change settings by typing in ```enable```.</br>
To ssh into the dev by itself it's just ```ssh amakhosa@139.178.91.146```.

### Creating tunnel in Umbrella
Login to Umbrella and under **Deployments** go to **Networks** and add a network based on how many devices wil be on it. For this example it will only be the one ASAv so name it and for the *IPv4 Address* put in a IP that fits into the network given by the dev environment.
For this case 139.178.91.147/32 was used. Save that and go to **Network Tunnels**.</br>
Under **Network Tunnels** click **Add** and name it whatever you want, but make sure you choose *ASA* for device type and choose the network you just created. Now the ASAv will go through Umbrella DC's before out to the internet.

### Sending traffic through the ASAv
Now that the ASAv is connected to the Umbrella DC's, we can route traffic through it. Depending on which DC you're connected to, you'll route through a different IP. In this case it is DFW which has a headend IP of 146.112.72.8 so we would type ```traceroute -s 172.31.6.72 8.8.8.8``` and see that it does some secret hops before exiting into LA and landing at Google's public DNS server.
