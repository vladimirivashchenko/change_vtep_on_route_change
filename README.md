(C) Vladimir Ivashchenko 2023 http://www.hazard.maks.net CC0 license

change_vtep_on_route_change is a Huawei OPS Python script that changes VTEP peer IP in case route to primary VTEP goes down. Tested on CloudEngine CE6800 switches.

The script is configured using up to 100 changevtep_targetsN environment variables. 

Below is an example config that monitors routes 10.1.1.0/30 used by VNI 10 and 10.2.3.0/30 used by VNI 20 (note that /30 prefix size is implied). When these routes will get added or removed from the routing table the script will configure VNIs under Nve1 interface with specified VTEPs.

<pre>
ops
 script-assistant python change_vtep_on_route_change.py
 environment changevtep_targets0 vni=10;monitor_net=10.1.1.0;add=10.1.1.1;remove=10.100.100.1
 environment changevtep_targets1 vni=20;monitor_net=10.2.3.0;add=10.2.3.1;remove=10.200.200.1
</pre>

Multiple targets can also be specified in the same environment variable using / separator.
