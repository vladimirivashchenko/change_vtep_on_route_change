change_vtep_on_route_change is a Huawei OPS Python script that changes VTEP peer IP in case route to primary VTEP goes down. Tested on CloudEngine CE6800 switches.

The script is configured using up to 100 changevtep_targetsN environment variables. 

Example config that monitors add/remove events for route 10.1.1.0/30 used by VNI 10 and 10.2.3.0/30 used by VNI 20 and configures specified VTEPs in case route gets added or removed from the routing table:

<pre>
ops
 script-assistant python change_vtep_on_route_change.py
 environment changevtep_targets0 monitor_net=10.1.1.0;vni=10;add=10.1.1.1;remove=10.100.100.1
 environment changevtep_targets1 monitor_net=10.2.3.0;vni=20;add=10.2.3.1;remove=10.200.200.1
</pre>

Multiple targets can also be specified in the same environment variable using / separator.
