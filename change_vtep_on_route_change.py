#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2023 Vladimir Ivashchenko v@ivashchenko.org https://www.hazard.maks.net CC0 license
import ops
import sys
import os

def ops_condition(_ops):
        # Get targets from OPS environment from up to 100 changevtep_targetsN environment variables. Multiple targets can be specified in the same variable using / separator
        targets = ""
        for x in range(100):
                envvar = "changevtep_targets" + str(x)
                envval, errstr = _ops.environment.get(envvar)
                envval = str(envval)
                if 'net=' in envval:
                        if targets is not "":
                                targets = targets + "/"
                        targets = targets + str(envval)

        status, err_log = _ops.syslog("Starting with parameters: " + targets, ops.INFORMATIONAL, ops.SYSLOG);

        i = 0
        known_routes = dict()
        opscorrelate = ""
        for target in targets.split("/"):
                if 'net=' not in target:
                        continue

                i = i + 1
                d = dict(x.split("=") for x in target.split(";"))

                status, err_log = _ops.syslog("Monitoring target route " + d["net"] + " for VNI " + d["vni"], ops.INFORMATIONAL, ops.SYSLOG);

                if d["net"] not in known_routes:
                        value, err_str = _ops.route.subscribe("changevtep" + str(i), d["net"], 30)
                        if 'OK' not in err_str:
                                status, err_log = _ops.syslog("!! Failed to monitor target route " + d["net"] + ": " + err_str, ops.INFORMATIONAL, ops.SYSLOG);
                        else:
                                known_routes[d["net"]] = 1
                                if opscorrelate is not "":
                                        opscorrelate = opscorrelate + " or "
                                opscorrelate = opscorrelate + "changevtep" + str(i)

        status, err_log = _ops.syslog("Finished startup process", ops.INFORMATIONAL, ops.SYSLOG);

        value, err_str = _ops.correlate(opscorrelate)

        return 0

def ops_execute(_ops):
        # Get targets from OPS environment
        targets = ""
        for x in range(100):
                envvar = "changevtep_targets" + str(x)
                envval, errstr = _ops.environment.get(envvar)
                envval = str(envval)
                if 'net=' in envval:
                        if targets is not "":
                                targets = targets + "/"
                        targets = targets + str(envval)

        # environment dynamically set by OPS for route change events
        rnetwork,errstr = _ops.environment.get("_routing_network")
        # remove, add, modify(?)
        rtype,errstr = _ops.environment.get("_routing_type")

        i = 0
        worked = 0
        for target in targets.split("/"):
                if 'net=' not in target:
                        continue

                i = i + 1

                d = dict(x.split("=") for x in target.split(";"))

                if rnetwork == d["net"] and rtype in d:
                        status, err_log = _ops.syslog("Acting on VTEP route change '" + rtype + "' for " + rnetwork + ", setting VNI " + d["vni"] + " VTEP to " + d[rtype], ops.CRITICAL, ops.SYSLOG)
                        # Open the CLI channel.
                        if worked == 0:
                                handle, err_desp = _ops.cli.open()
                        # Run the system-view command to enter the system view.
                        result, n11, n21 = _ops.cli.execute(handle,"system-view")
                        result, n11, n21 = _ops.cli.execute(handle,"interface Nve1")
                        result, n11, n21 = _ops.cli.execute(handle,"undo vni " + d["vni"])
                        result, n11, n21 = _ops.cli.execute(handle,"vni " + d["vni"] + " head-end peer-list " + d[rtype])
                        if result:
                                status, err_log = _ops.syslog("!! Error configuring NVI under Nve1 !!", ops.CRITICAL, ops.SYSLOG)
                        result, n11, n21 = _ops.cli.execute(handle,"commit")
                        worked = 1

        status, err_log = _ops.syslog("Triggering an informational SNMP event", ops.CRITICAL, ops.SYSLOG)
        if worked == 1:
                ret = _ops.cli.close(handle)

        return 0

