# How to set up an IPSec tunnel in Linux to Umbrella

## 1. Create a tunnel in the Umbrella dashboard
Log-in to Umbrella and under **Deployments** click on **Network Tunnels**. There should be an **Add** button; click it. Name the tunnel whatever you want, but choose other for device type. Click create and take note of the tunnel ID and PSK.

## 2. Configuration
On the linux terminal install strongswan with ```apt-get install strongswan``` (Note: may need to put ```sudo``` first). Now go to the etc directory with ```cd /etc``` and create a file named *ipsec.conf* (Use the command ```vi ipsec.conf```). Now copy paste this code into the file:
```
#/etc/ipsec.conf
config setup
    # silence all the loggind, we do not need it
    charondebug="chd -1, ike -1, knl -1, cfg -1, net -1, esp -1, dmn -1, mgr -1"config setup
config setup
conn %default
    keyingtries=%forever
    keyexchange=ikev2
conn TUNNEL_NAME_HERE
    auto=add
    esp=aes256-sha1!
    ike=aes256-sha1-modp3072!
    left=%any
    leftid=TUNNEL_ID_HERE
    leftauth=psk
    leftsubnet=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,198.18.0.0/24
    right=HEADEND_PUBLIC_IP_HERE
    rightid=cvpn
    rightsubnet=0.0.0.0/0
    rightauth=psk
    mark=64
```
Put the the tunnel name and ID in their respective places, and replace HEADEND_PUBLIC_IP_HERE with an ip found on the internal list, i.e. 146.112.66.8 for Palo Alto, CA.

The next thing to do is edit *charon.conf*. Enter ```vi /etc/strongswan.d/charon.conf``` and copy/paste the following:
```
#/etc/strongswan.d/charon.conf
# Options for the charon IKE daemon.
charon {

    # Initiate IKEv2 reauthentication with a make-before-break instead of
    # a break-before-make scheme. Make-before-break uses overlapping IKE and
    # CHILD_SA during reauthentication by first recreating all new SAs before
    # deleting the old ones. This behavior can be beneficial to avoid
    # connectivity gaps during reauthentication, but requires support for
    # overlapping SAs by the peer. strongSwan can handle such overlapping SAs since 5.3.0.
    make_before_break = yes

    # Close the IKE_SA if setup of the CHILD_SA along with IKE_AUTH failed.
    close_ike_on_child_failure = yes

    # Timeout in seconds for connecting IKE_SAs (also see IKE_SA_INIT DROPPING).
    half_open_timeout = 30

    # Causes charon daemon to ignore IKE initiation requests.
    initiator_only = yes

    # Install routes into a separate routing table for established IPsec
    # tunnels.
    install_routes = no

    # Install virtual IP addresses.
    install_virtual_ip = no

    # UDP port used locally. If set to 0 a random port will be allocated.
    port = 500

    # UDP port used locally in case of NAT-T. If set to 0 a random port will be
    # allocated.  Has to be different from charon.port, otherwise a random port
    # will be allocated.
    port_nat_t = 4500

    # Number of times to retransmit a packet before giving up.
    retransmit_tries = 0

    # Number of worker threads in charon.
    threads = 32

    crypto_test {

    }

    host_resolver {

    }

    leak_detective {

    }

    processor {

        # Section to configure the number of reserved threads per priority class
        # see JOB PRIORITY MANAGEMENT in strongswan.conf(5).
        priority_threads {

        }

    }

    # Section containing a list of scripts (name = path) that are executed when
    # the daemon is started.
    start-scripts {

    }

    # Section containing a list of scripts (name = path) that are executed when
    # the daemon is terminated.
    stop-scripts {

    }

    tls {

    }

    x509 {

    }

}
```
Make sure ```port_nat_t = 4500``` and ```port = 500```.
The last step in configuration is to enter ```vi /etc/ipsec.secrets``` and enter your PSK (Note: may need to sudo to actually see anything).
```
#This file holds shared secrets or RSA private keys for authentication.

#RSA private key for this host, authenticating it to any other host
#which knows the public part.

%any : PSK PSK_HERE
```

## 3. Connecting and checking tunnel
Make sure to turn off any other VPN you may have on and type ```ipsec start``` to connect. To check status of connection use ```ipsec status``` and ```ipsec stop``` to stop. Check ```ipsec --help``` for other useful things.
