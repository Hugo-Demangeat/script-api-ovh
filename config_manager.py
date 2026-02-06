import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

DEFAULTS = {
    "NIC": "VOTRE_NIC",
    "APPLICATION_KEY": "VOTRE_APP_KEY",
    "APPLICATION_SECRET": "VOTRE_APP_SECRET",
    "CONSUMER_KEY": "VOTRE_CONS_KEY",
    "ENDPOINT": "ovh-eu",
    "OVH_SUBSIDIARY": "FR",
    "OWNER_CONTACT": "/me/contact/123456",
    "PAYMENT_METHOD": "preferred",
    "AUTO_BUY": False,
    "AUTO_DNS": True,
    "CUSTOM_DNS": ""
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULTS)
        return DEFAULTS.copy()
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
