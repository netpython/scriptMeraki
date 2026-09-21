# scriptMeraki

Collection de 15 scripts Python pour auditer et exploiter une organisation Cisco Meraki via Dashboard API.

## Scripts

| # | Script | Fonction |
|---|---|---|
| 01 | `01_organization_inventory.py` | Inventaire complet des réseaux et équipements |
| 02 | `02_network_selector.py` | Menu des réseaux filtrable par tags |
| 03 | `03_device_health.py` | Santé des switches, AP et appliances |
| 04 | `04_firmware_audit.py` | Versions firmware par réseau et produit |
| 05 | `05_switch_ports.py` | État, VLAN, PoE et voisin des ports MS |
| 06 | `06_poe_audit.py` | Consommation et capacité PoE des ports d'accès |
| 07 | `07_ap_ip_mode.py` | Bornes en IP statique ou DHCP |
| 08 | `08_uplink_downlink_audit.py` | Audit des équipements tagués uplink/downlink |
| 09 | `09_lldp_cdp_topology.py` | Export de la topologie LLDP/CDP |
| 10 | `10_clients_audit.py` | Clients récents par réseau |
| 11 | `11_ssid_audit.py` | Configuration des SSID sans secrets |
| 12 | `12_mx_vlan_audit.py` | VLAN et sous-réseaux MX |
| 13 | `13_alerts_audit.py` | Paramètres d'alertes des réseaux |
| 14 | `14_config_backup.py` | Sauvegarde JSON des configurations principales |
| 15 | `15_live_monitor.py` | Supervision live, deux tableaux, mode alertes-only |

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yml config.yml
export MERAKI_DASHBOARD_API_KEY='votre-cle-api'
```

## Exemples

```bash
python scripts/01_organization_inventory.py
python scripts/05_switch_ports.py --network-id L_123456
python scripts/07_ap_ip_mode.py
python scripts/15_live_monitor.py --alerts-only --refresh 60
```

Les exports sont écrits dans `outputs/` aux formats CSV, JSON ou XLSX. Les scripts respectent les limites API Meraki grâce au SDK officiel.

## Principes de sécurité

- La clé API est lue uniquement depuis `MERAKI_DASHBOARD_API_KEY`.
- Aucun secret n'est exporté.
- Les scripts fournis sont en lecture seule.
- `config.yml`, `outputs/` et `logs/` sont exclus de Git.

## Licence

MIT.

## Programmes avancés

Le dossier `programs/` contient cinq audits complets : conformité organisationnelle, capacité/PoE, sécurité Wi-Fi, Client Explorer et firmware/cycle de vie.
