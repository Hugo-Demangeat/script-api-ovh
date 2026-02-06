import ovh
from util import demander_input, choisir_parmi, handle_api_error, afficher_resume_panier
from domain import valider_nom_domaine
import config_manager
import sys

def parametrage():
    print("\n=== Paramétrage OVH ===")
    cfg = config_manager.load_config()
    # Saisie des paramètres principaux
    cfg["NIC"] = demander_input(f"NIC OVH [{cfg['NIC']}]:\n", cfg["NIC"])
    cfg["APPLICATION_KEY"] = demander_input(f"Application Key [{cfg['APPLICATION_KEY']}]:\n", cfg["APPLICATION_KEY"])
    cfg["APPLICATION_SECRET"] = demander_input(f"Application Secret [{cfg['APPLICATION_SECRET']}]:\n", cfg["APPLICATION_SECRET"])
    cfg["CONSUMER_KEY"] = demander_input(f"Consumer Key [{cfg['CONSUMER_KEY']}]:\n", cfg["CONSUMER_KEY"])
    cfg["ENDPOINT"] = demander_input(f"Endpoint [{cfg['ENDPOINT']}]:\n", cfg["ENDPOINT"])
    cfg["OVH_SUBSIDIARY"] = demander_input(f"Filiale OVH [{cfg['OVH_SUBSIDIARY']}]:\n", cfg["OVH_SUBSIDIARY"])

    # Afficher et choisir un contact existant
    import ovh
    client = ovh.Client(
        endpoint=cfg["ENDPOINT"],
        application_key=cfg["APPLICATION_KEY"],
        application_secret=cfg["APPLICATION_SECRET"],
        consumer_key=cfg["CONSUMER_KEY"]
    )
    try:
        contacts = client.get("/me/contact")
        if not contacts:
            print("Aucun contact trouvé sur le compte OVH.")
            val = demander_input(f"Contact propriétaire (ex: /me/contact/123456) [{cfg['OWNER_CONTACT']}]:\n", cfg["OWNER_CONTACT"])
            cfg["OWNER_CONTACT"] = val if val else cfg["OWNER_CONTACT"]
        else:
            contact_labels = []
            contact_map = {}
            for cid in contacts:
                try:
                    c = client.get(f"/me/contact/{cid}")
                    lbl = f"{c.get('nicHandle')} - {c.get('firstName','')} {c.get('lastName','')} ({c.get('email','')})"
                except:
                    lbl = str(cid)
                contact_labels.append(lbl)
                contact_map[lbl] = cid
            print("Choisissez le contact propriétaire :")
            for i, opt in enumerate(contact_labels, 1):
                print(f"{i}. {opt}")
            choix = input("Entrez un numéro :\n").strip()
            try:
                idx = int(choix) - 1
                if 0 <= idx < len(contact_labels):
                    cfg["OWNER_CONTACT"] = f"/me/contact/{contact_map[contact_labels[idx]]}"
                else:
                    # Choix invalide, garder l'actuel
                    pass
            except:
                # Entrée vide ou invalide, garder l'actuel
                pass
    except Exception as e:
        print("Erreur lors de la récupération des contacts OVH :", e)
        val = demander_input(f"Contact propriétaire (ex: /me/contact/123456) [{cfg['OWNER_CONTACT']}]:\n", cfg["OWNER_CONTACT"])
        cfg["OWNER_CONTACT"] = val if val else cfg["OWNER_CONTACT"]

    # Sélection du moyen de paiement
    try:
        payment_methods = client.get("/me/payment/method")
        if not payment_methods:
            print("Aucun moyen de paiement trouvé sur le compte OVH.")
            val = demander_input(f"Moyen de paiement (ex: preferred) [{cfg['PAYMENT_METHOD']}]:\n", cfg["PAYMENT_METHOD"])
            cfg["PAYMENT_METHOD"] = val if val else cfg["PAYMENT_METHOD"]
        else:
            payment_labels = []
            payment_map = {}
            for pm_id in payment_methods:
                try:
                    pm = client.get(f"/me/payment/method/{pm_id}")
                    label = f"{pm.get('paymentMean', pm_id)} - {pm.get('description', '')} (id: {pm_id})"
                except:
                    label = str(pm_id)
                payment_labels.append(label)
                payment_map[label] = pm_id
            print("Choisissez le moyen de paiement :")
            for i, opt in enumerate(payment_labels, 1):
                print(f"{i}. {opt}")
            choix_pm = input("Entrez un numéro :\n").strip()
            try:
                idx = int(choix_pm) - 1
                if 0 <= idx < len(payment_labels):
                    cfg["PAYMENT_METHOD"] = payment_map[payment_labels[idx]]
                else:
                    # Choix invalide, garder l'actuel
                    pass
            except:
                # Entrée vide ou invalide, garder l'actuel
                pass
    except Exception as e:
        print("Erreur lors de la récupération des moyens de paiement OVH :", e)
        val = demander_input(f"Moyen de paiement (ex: preferred) [{cfg['PAYMENT_METHOD']}]:\n", cfg["PAYMENT_METHOD"])
        cfg["PAYMENT_METHOD"] = val if val else cfg["PAYMENT_METHOD"]

    # Paramétrage AUTO_BUY avec choix 1/2, garder l'actuel si entrée vide ou invalide
    print("Souhaitez-vous activer l'achat automatique (payer directement) ?")
    auto_buy_options = ["Oui", "Non"]
    actuel = 'Oui' if cfg.get('AUTO_BUY', False) else 'Non'
    print(f"Achat automatique ? [Actuel: {actuel}]")
    for i, opt in enumerate(auto_buy_options, 1):
        print(f"{i}. {opt}")
    choix_auto = input("Entrez un numéro :\n").strip()
    try:
        idx = int(choix_auto) - 1
        if idx == 0:
            cfg["AUTO_BUY"] = True
        elif idx == 1:
            cfg["AUTO_BUY"] = False
        else:
            # Choix invalide, garder l'actuel
            pass
    except:
        # Entrée vide ou invalide, garder l'actuel
        pass

    # Paramétrage AUTO_DNS
    print("Souhaitez-vous utiliser la configuration DNS automatique d'OVH ?")
    auto_dns_options = ["Oui", "Non"]
    actuel_dns = 'Oui' if cfg.get('AUTO_DNS', True) else 'Non'
    print(f"DNS automatique ? [Actuel: {actuel_dns}]")
    for i, opt in enumerate(auto_dns_options, 1):
        print(f"{i}. {opt}")
    choix_dns = input("Entrez un numéro :\n").strip()
    try:
        idx = int(choix_dns) - 1
        if idx == 0:
            cfg["AUTO_DNS"] = True
        elif idx == 1:
            cfg["AUTO_DNS"] = False
        else:
            pass
    except:
        pass

    # Si AUTO_DNS désactivé, demander le DNS personnalisé
    if not cfg.get("AUTO_DNS", True):
        val = demander_input(f"Adresse DNS personnalisée (séparées par virgule) [{cfg.get('CUSTOM_DNS','')}]:\n", cfg.get("CUSTOM_DNS", ""))
        cfg["CUSTOM_DNS"] = val if val is not None else cfg.get("CUSTOM_DNS", "")

    config_manager.save_config(cfg)
    print("\n✅ Paramètres sauvegardés dans config.json (persistant et portable)")

def acheter_domaine():
    cfg = config_manager.load_config()
    client = ovh.Client(
        endpoint=cfg["ENDPOINT"],
        application_key=cfg["APPLICATION_KEY"],
        application_secret=cfg["APPLICATION_SECRET"],
        consumer_key=cfg["CONSUMER_KEY"]
    )
    try:
        client.get("/me")
    except Exception as e:
        handle_api_error(e, "vérification clés API")
    print("✅ Clés valides.\n")

    dn = demander_input("Nom de domaine à commander :\n")
    if not valider_nom_domaine(dn):
        print("❌ Domaine invalide.")
        sys.exit(1)

    print(f"📍 Création du panier et vérification de la disponibilité pour {dn}…")
    try:
        cart = client.post("/order/cart", ovhSubsidiary=cfg["OVH_SUBSIDIARY"], description="Commande auto script")
        cart_id = cart["cartId"]
        client.post(f"/order/cart/{cart_id}/assign", nic=cfg["NIC"])
        offers = client.get(
            f"/order/cart/{cart_id}/domain",
            domain=dn
        )
    except Exception as e:
        handle_api_error(e, "récupération des offres disponibles")

    offers_create = [off for off in offers if off.get("action", "").startswith("create")]
    if not offers_create:
        print(f"❌ Le domaine {dn} n’est pas disponible pour enregistrement.")
        print("➡️ Il peut être transféré si tu en es propriétaire.")
        sys.exit(0)


    # Si une seule offre 'create', on passe directement à la sélection de la durée
    if len(offers_create) == 1:
        offer = offers_create[0]
        print("\n--- Offre ---")
        plan = offer.get("offerId") or offer.get("planCode")
        print(f"PlanCode: {plan}")
        print(f"Durations: {offer.get('duration')}")
        for p in offer.get("prices", []):
            print(f"  {p.get('label')} -> {p.get('price', {}).get('text')}")
    else:
        print("\n📊 Offres disponibles :")
        offer_strings=[]
        for i, off in enumerate(offers_create, 1):
            print(f"\n--- Offre {i} ---")
            plan = off.get("offerId") or off.get("planCode")
            print(f"PlanCode: {plan}")
            print(f"Durations: {off.get('duration')}")
            for p in off.get("prices", []):
                print(f"  {p.get('label')} -> {p.get('price', {}).get('text')}")
            offer_strings.append(f"{i}. {off.get('action')}")
        choice = choisir_parmi("\nChoisis une offre :", offer_strings)
        idx = int(choice.split(".")[0]) - 1
        offer = offers_create[idx]

    duration = choisir_parmi("Choisis durée :", offer["duration"])
    pricing_mode = offer["pricingMode"]
    plan_code = offer.get("offerId") or demander_input("Plan Code:\n","fr")

    # Ajout du domaine au panier
    try:
        added = client.post(
            f"/order/cart/{cart_id}/domain",
            domain=dn,
            duration=duration,
            planCode=plan_code,
            pricingMode=pricing_mode
        )
        item_id = added["itemId"]
        # Configuration propriétaire
        client.post(
            f"/order/cart/{cart_id}/item/{item_id}/configuration",
            label="OWNER_CONTACT",
            value=cfg["OWNER_CONTACT"]
        )
        # Configuration DNS personnalisé si demandé
        if not cfg.get("AUTO_DNS", True) and cfg.get("CUSTOM_DNS", ""):
            # On suppose que l'utilisateur entre les DNS séparés par des virgules
            dns_list = [dns.strip() for dns in cfg["CUSTOM_DNS"].split(",") if dns.strip()]
            for idx, dns in enumerate(dns_list, 1):
                client.post(
                    f"/order/cart/{cart_id}/item/{item_id}/configuration",
                    label=f"DNS{idx}",
                    value=dns
                )
        checkout = client.get(f"/order/cart/{cart_id}/checkout")
        afficher_resume_panier(checkout)
        if cfg.get("AUTO_BUY", False):
            confirm = "oui"
        else:
            confirm = demander_input("\nCréer & payer la commande ? (oui/non):\n","non").lower()
        if confirm == "oui":
            if cfg.get("AUTO_BUY", False):
                sales_order = client.post(
                    f"/order/cart/{cart_id}/checkout",
                    autoPayWithPreferredPaymentMethod=True,
                    waiveRetractationPeriod=True
                )
                print(f"\n🎉 Commande finalisée et payée : {sales_order.get('orderId')}")
            else:
                sales_order = client.post(
                    f"/order/cart/{cart_id}/checkout"
                )
                print(f"\n📝 Commande créée (à régler sur OVH) : {sales_order.get('orderId')}")
        else:
            print("\n❗ Commande annulée.")
    except Exception as e:
        handle_api_error(e, "commande domaine")

def main():
    while True:
        print("=== Script OVH Achat Domaine Automatique ===")
        choix = choisir_parmi("Que voulez-vous faire ?", ["Acheter un domaine", "Paramétrage", "Quitter"])
        try:
            if choix == "Acheter un domaine":
                acheter_domaine()
            elif choix == "Paramétrage":
                parametrage()
            else:
                print("Au revoir !")
                break
        except Exception as e:
            if str(e) == "RetourMenuPrincipal":
                continue
            else:
                raise

if __name__ == "__main__":
    main()
