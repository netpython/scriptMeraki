#!/usr/bin/env python3
from common import *
log=setup("clients_audit"); p=base_parser("Clients Meraki"); p.add_argument("--timespan",type=int,default=86400); args=p.parse_args(); cfg=config(args.config); api=dashboard(); oid=org_id(cfg); n=choose_network(api,oid)
clients=api.networks.getNetworkClients(n["id"],timespan=args.timespan,total_pages="all"); rows=[{"network":n["name"],"description":x.get("description"),"mac":x.get("mac"),"ip":x.get("ip"),"vlan":x.get("vlan"),"status":x.get("status"),"usageSent":x.get("usage",{}).get("sent"),"usageRecv":x.get("usage",{}).get("recv")} for x in clients]
log.info("Export: %s",write_csv("clients",rows))

