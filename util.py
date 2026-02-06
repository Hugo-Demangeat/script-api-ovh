import re
import sys

def demander_input(message, valeur_par_defaut=None):
    val = input(message).strip()
    return val if val else valeur_par_defaut

def choisir_parmi(message, options):
    print(message)
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choix = input("Entrez un numéro :\n").strip()
    try:
        idx = int(choix) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except:
        pass
    print("⚠️ Choix invalide, on prend la première option.")
    return options[0]

def handle_api_error(e, contexte=""):
    print(f"\n❌ Erreur API OVH pendant : {contexte}")
    status = getattr(e, "http_status", None)
    if status == 400: print("→ Requête invalide (HTTP 400).")
    elif status == 401: print("→ Authentification invalide.")
    elif status == 403: print("→ Accès interdit.")
    elif status == 404: print("→ Ressource introuvable.")
    elif status == 409: print("→ Conflit (déjà existant).")
    else: print(f"→ Message OVH : {e}")
    print("\nRetour au menu principal...\n")
    raise Exception("RetourMenuPrincipal")

def afficher_resume_panier(checkout):
    print("\n=== Récapitulatif (dry‑run) ===")
    for item in checkout.get('items', []):
        print(f"- {item['productId']} : {item['prices'][-1]['price']['text']}")
    total = checkout['prices']['withTax']['value']
    print(f"💰 Total TTC : {total} {checkout['prices']['withTax']['currencyCode']}")
