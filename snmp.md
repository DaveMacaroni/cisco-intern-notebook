# Getting familiar with SNMP
This was the final onboarding task. Everything that has been done was building up to this. The goal was to set up snmp on an ASAv and send those metrics to Prometheus.

### How SNMP works
SNMP stands for Simple Network Management Protocol, and it gathers metrics of a device in real-time. There are two main components to it: OID's and MIB's.</br>

OID stands for Object Identifier and every device that can be monitored by SNMP has an OID. They are organized in a tree structure with the left most number being the root. An example of an OID list is:
```
"org"		"1.3"
"dod"		"1.3.6"
"internet"		"1.3.6.1"
"directory"		"1.3.6.1.1"
"mgmt"		"1.3.6.1.2"
"experimental"		"1.3.6.1.3"
"private"		"1.3.6.1.4"
"enterprises"		"1.3.6.1.4.1"
"cisco"		"1.3.6.1.4.1.9"
"ciscoMgmt"		"1.3.6.1.4.1.9.9"
"ciscoIpSecFlowMonitorMIB"		"1.3.6.1.4.1.9.9.171"
"cipSecMIBObjects"		"1.3.6.1.4.1.9.9.171.1"
"cipSecMIBNotificationPrefix"		"1.3.6.1.4.1.9.9.171.2"
"cipSecMIBConformance"		"1.3.6.1.4.1.9.9.171.3"
"cipSecLevels"		"1.3.6.1.4.1.9.9.171.1.1"
"cipSecPhaseOne"		"1.3.6.1.4.1.9.9.171.1.2"
"cipSecPhaseTwo"		"1.3.6.1.4.1.9.9.171.1.3"
"cipSecHistory"		"1.3.6.1.4.1.9.9.171.1.4"
"cipSecFailures"		"1.3.6.1.4.1.9.9.171.1.5"
"cipSecTrapCntl"		"1.3.6.1.4.1.9.9.171.1.6"
"cipSecMibLevel"		"1.3.6.1.4.1.9.9.171.1.1.1"
"cikeGlobalStats"		"1.3.6.1.4.1.9.9.171.1.2.1"
"cikePeerTable"		"1.3.6.1.4.1.9.9.171.1.2.2"
"cikeTunnelTable"		"1.3.6.1.4.1.9.9.171.1.2.3"
"cikePeerCorrTable"		"1.3.6.1.4.1.9.9.171.1.2.4"
"cikePhase1GWStatsTable"		"1.3.6.1.4.1.9.9.171.1.2.5"
"cikeGlobalActiveTunnels"		"1.3.6.1.4.1.9.9.171.1.2.1.1"
"cikeGlobalPreviousTunnels"		"1.3.6.1.4.1.9.9.171.1.2.1.2"
```

MIB stands for Management Information Base and it is a file that turns OIDs from numbers into names. For example, the OIDs above come from a list called **CISCO-IPSEC-FLOW-MONITOR-MIB**, so when you configure snmp to use MIBs and request the OID **1.3.6.1.4.1.9.9.171.1.2.1.1**, SNMP would show you **CISCO-IPSEC-FLOW-MONITOR-MIB::cikeGlobalActiveTunnels.0** instead. The format is *Module::OID.InterfaceID*. MIBs are enabled in snmp.conf which will be shown later.</br>

The NMS is the Network Management Station and this is where you get SNMP metrics (in this case the NMS is the Debian host). 
By default SNMP will send metrics to port 161 and the NMS will "poll" the SNMP device to get the metrics at that given instance. SNMP can be configured to send traps that will alert a user if something happens, but this is already done via prometheus/alert manager so we wil not go into how to set that up.

### Setting up and viewing SNMP
Configuration for snmp devices are found in manuals for said device. For the ASA, the setup is [here](https://www.cisco.com/c/en/us/td/docs/security/asa/asa90/configuration/guide/asa_90_cli_config/monitor_snmp.html#30757).
Note that this is for version 2c of SNMP. This was done out of simplicity and because 2c is usually good enough, however if ever being used in production, consider using version 3 because it allows encryption and authentication.</br>

Setting up snmp on the ASA is straightforward. First ```enable``` and then ```conf t``` to enter configuration mode. Then type:
```
snmp-server host internal 172.31.6.254 community *WORD* version 2c
```
This is telling the snmp-server that the snmp host (the ASA) will be monitoring the internal interface with an IP inside the internal network, and it has a community string of whatever is put there all while using version 2c of SNMP (Version 1 and 2c of SNMP use community strings, version 3 uses usernames and passwords).
You can also specify what udp-port to send to but the default for this version of the ASA is 162. Now in the Debian host you can type:
```
snmpwalk -v 2c -c *WORD* 172.31.6.2
```
> May need to configure firewall or routing table to allow this IP through

Where 172.31.6.2 is the IP of the internal interface on the ASA. You can also specify after the IP what OID you want to walk, but for the case of setting up SNMP this is just a way to see that it works. For now the OIDs are all numerical, but the snmp exporter will convert the numerical OIDs to human readable ones when we set that up.</br>

If you want to see snmp metrics in readable text in the console, find a MIB support list for that device and pick which MIBs you want. Then use Cisco's [MIB Locator](https://cfnng.cisco.com/mibs) (alternative link that shows dependancies list [here](https://snmp.cloudapps.cisco.com/Support/SNMP/do/BrowseMIB.do?local=en&step=2)). Since we used version 2c, click on the **V2** button and place these in a directory dedicated to these MIBs. Then ```vi /etc/snmp/snmp.conf``` and comment out the line that has ```mibs :``` and at the bottom write:
```
mibdirs /path/to/mib/directory
```
You may also have to write ```export MIBS=ALL``` into your *.bashrc*. Also note that some MIBs have dependancies on other MIB files so they would also need to be downloaded. When you snmpwalk, it will be specified at the top of the results which files are missing.

### Setting up SNMP Exporter
The snmp exporter can be found [here](https://github.com/prometheus/snmp_exporter). Download the correct binary and when you unzip it there should be 4 files: *LICENSE*, *NOTICE*, *snmp_exporter*, and *snmp.yml*. The *snmp.yml* file is what snmp exporter reads to turn the OIDs from numerical to human readable, but to write one ourselves would take forever. Luckily we can use the [generator](https://github.com/prometheus/snmp_exporter/tree/master/generator).</br>

Follow the instructions to download the generator and open *generator.yml*. This file is the one you write in that allows the generator to make a correctly formatted *snmp.yml* file for the exporter. A simple *generator.yml* file would look like this:
```
modules:
  IPSEC-FLOW:  
    walk:  #List of OIDs to walk
      - 1.3.6.1.4.1.9.9.171  #OID tree listed under CISCO-IPSEC-FLOW-MONITOR-MIB
    version: 2
    max_repetitions: 25  #How many objects to request with get/getbulk
    retries: 3
    timeout: 10ms
    auth:
      community: *WORD*
```
The amount of modules you write shouldn't matter because these metrics are going to be sent to Prometheus, but the walk section is where you write the OID branch that you want to walk down, and you can be as specific as you want ranging from thousands of OIDs to just one. Remember to ```export MIBDIRS=mibs``` so the generator can read the mibs and make the *snmp.yml* file</br>

Now you can run the generator with ```./generator generate``` and it will produce an *snmp.yml* file that you have to copy into the same directory as the snmp exporter.
Now you can run snmp exporter. To see if it works go to a web browser and check port 9116. There you can enter the target and the module you wish to see and most of the metrics should be there. Ex ```http://139.178.91.146:9116/snmp?target=172.31.6.2&module=IPSEC-FLOW```

### Sending metrics to Prometheus
Sending these metrics to prometheus is simple. All we need to do is add a job to the *prometheus.yml* file. It can look like this:
```
scrape_configs:
  - job_name: 'snmp'
    static_configs:
      - targets:
        - 172.31.6.2  # SNMP device.
    metrics_path: /snmp
    params:
      module: [IPSEC-FLOW]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9116  # The SNMP exporter's real hostname:port.
```
Prometheus reads the snmp exporter and displays the metrics accordingly.
