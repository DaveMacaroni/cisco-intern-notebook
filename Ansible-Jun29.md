# Installing GIT on a VM via Ansible
The goal of this task was to install git on a brand new Linux VM by using Ansible on a Mac host. Although after this task it seems easy to do, it started off terribly. 
### Problem:
Wasn't able to ping VM from Mac
### Solution:
```ifconfig``` on both terminals to see ip and tried ```ping``` to see if machines could talk, but they kept timing out. Made sure *Machine Settings > Network > Attatched to: Bridge Adapter* was enabled to *en0: Wireless* so that Vm actually had an IP.
Checked ```netstat -nr``` on Mac to see routing tables and looked for VM IP and found that it was going through *utun2* rather than *en0*. First tried ```sudo route -n add -net 10.0.0.250/32 -interface en0``` to add VM IP as a new route through en0 but still ended up timing out so previous line was undone by replacing *add* with *delete*. 
What was realized then was that AnyConnect (VPN) was running so that was disconnected and then ping was succesful. 



After that was fixed the next step was to give the VM the Mac's public key it generated with ```ssh-keygen```. The keys were stored in the *.ssh* folder so from there the public key was copied and in the VM a new file was created in directory *~/.ssh* named *authorized_keys*. In there the public key was pasted. The next step was to then see if I could SSH into the VM from a Mac host by typing ```ssh aman@10.0.0.250``` where the IP was that of the VM, and it was succesful. Now it was time to activate the ansible playbook. With 3 files: 
*inventory*
```
[local] #Can be named whatever
10.0.0.250 # LinuxVM_2
```
*ansible.cfg*
```
[defaults]
inventory = inventory
#transport = local #Commented bc it wasn't going to localhost
```
and *test.yml*
```
--- #yml has to start like this

- name: Hello test #First time using ansible was a hello echo
  hosts: local #Name of group
  gather_facts: False 
  tasks:
    - name: Echo hello 
      shell: echo "hello"
    - name: Install GIT
      shell: apt -y install git #-y is to say yes to installation
      become: yes #yes become root so I can install
```
### Problem:
```fatal: [10.0.0.250]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: amakhosa@10.0.0.250: Permission denied (publickey,password).", "unreachable": true}```
### Solution:
Typed ```ansible-playbook -e "ansible_user=aman" test.yml``` to run playbook test.yml, but add aman as a user when SSH-ing. Permanent fix would be to add that line into the actual file.
### Problem:
```fatal: [10.0.0.250]: FAILED! => {"msg": "Missing sudo password"}```
### Solution:
Much time was spent trying to fix this but this is what the solution was. In the VM go ```sudo vi /etc/sudoers``` and make it look like:
```

#
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
# See the man page for details on how to write a sudoers file.
#
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"

# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
#root   ALL=(ALL:ALL) ALL
%sudo ALL=(ALL) NOPASSWD: ALL

# Members of the admin group may gain root privileges
%admin ALL=(ALL) ALL

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL

# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d
```
Then ```cd /etc/sudoers.d``` and ```sudo touch aman``` followed by ```vi aman``` and in there paste ```aman ALL=(ALL) NOPASSWD: ALL```. Now if you SSH into the VM from the Mac and do ```sudo -i``` you should root without typing a password.


After that, type run the ansible playbook ```ansible-playbook test.yml``` in this case (if you added the ```ansible_user=aman``` line) and git is installed on a VM by using Ansible!

P.S. New commands learnt are: 
* ```ps ax``` to see history of processes
* ```history``` to see everything you typed
* ``` | grep``` to do a group search
