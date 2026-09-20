#!/usr/bin/env python3
"""Fonctions communes pour les scripts Meraki."""
from __future__ import annotations
import argparse, csv, json, logging, os
from datetime import datetime
from pathlib import Path
from typing import Any
import meraki, yaml

ROOT=Path(__file__).resolve().parents[1]; OUTPUT=ROOT/"outputs"; LOGS=ROOT/"logs"

def setup(name:str)->logging.Logger:
    OUTPUT.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(LOGS/f"{name}.log"),logging.StreamHandler()])
    return logging.getLogger(name)

def config(path:str="config.yml")->dict[str,Any]:
    p=Path(path); return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}

def dashboard()->meraki.DashboardAPI:
    key=os.getenv("MERAKI_DASHBOARD_API_KEY")
    if not key: raise SystemExit("Définir MERAKI_DASHBOARD_API_KEY.")
    return meraki.DashboardAPI(key,suppress_logging=True,print_console=False,wait_on_rate_limit=True,maximum_retries=5)

def org_id(cfg:dict[str,Any])->str:
    value=str(cfg.get("organization_id","")).strip()
    if not value: raise SystemExit("Renseigner organization_id dans config.yml.")
    return value

def base_parser(description:str)->argparse.ArgumentParser:
    p=argparse.ArgumentParser(description=description); p.add_argument("-c","--config",default="config.yml"); return p

def stamp()->str: return datetime.now().strftime("%Y%m%d_%H%M%S")

def write_json(name:str,data:Any)->Path:
    path=OUTPUT/f"{name}_{stamp()}.json"; path.write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str),encoding="utf-8"); return path

def write_csv(name:str,rows:list[dict[str,Any]])->Path:
    path=OUTPUT/f"{name}_{stamp()}.csv"; fields=sorted({k for r in rows for k in r}) or ["result"]
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    return path

def networks(api,oid:str)->list[dict[str,Any]]: return sorted(api.organizations.getOrganizationNetworks(oid,total_pages="all"),key=lambda x:x["name"].lower())

def choose_network(api,oid:str,tags:list[str]|None=None)->dict[str,Any]:
    items=networks(api,oid)
    if tags: items=[n for n in items if set(tags)&set(n.get("tags",[]))]
    for i,n in enumerate(items,1): print(f"{i:>3}. {n['name']}  [{', '.join(n.get('tags',[]))}]")
    while True:
        try: return items[int(input("Numéro du réseau : "))-1]
        except (ValueError,IndexError): print("Sélection invalide.")

def network_name_map(api,oid:str)->dict[str,str]: return {n["id"]:n["name"] for n in networks(api,oid)}

