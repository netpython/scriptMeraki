#!/usr/bin/env python3
from common import *
p=base_parser("Sélection de réseau par numéro et tags"); p.add_argument("--tags",nargs="*"); args=p.parse_args(); cfg=config(args.config); api=dashboard()
n=choose_network(api,org_id(cfg),args.tags or cfg.get("network_tags")); print(json.dumps(n,indent=2,ensure_ascii=False))

