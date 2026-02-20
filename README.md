# Script d’Achat Automatique de Domaine OVH (Python)

## Résumé du programme

Ce projet propose un script Python en ligne de commande permettant :

- De configurer facilement les paramètres d’accès à l’API OVH (identifiants, contacts, moyens de paiement, DNS…)
- D’acheter automatiquement un nom de domaine disponible chez OVH, avec gestion du panier, du propriétaire, du paiement et des DNS personnalisés
- De centraliser la configuration dans un fichier `config.json` pour une utilisation récurrente et portable

Ce script vise à automatiser et simplifier l’achat de domaines OVH pour les développeurs, administrateurs ou intégrateurs.

---

## Prérequis

- Python 3.7 ou supérieur
- La bibliothèque officielle OVH pour Python : `ovh`
- Un compte OVH avec :
  - Un identifiant NIC
  - Des clés API (Application Key, Application Secret, Consumer Key) générées sur OVH API
  - Un moyen de paiement enregistré

---

## Installation

1. Installer Python (https://www.python.org/)
2. Installer la dépendance OVH :
   ```bash
   pip install ovh
   ```
3. Placer tous les fichiers du projet dans le même dossier
4. Le fichier `config.json` sera créé automatiquement au premier lancement si absent

---

## Utilisation

Dans le dossier du script, lancez :

```bash
python auto_domain.py
```

Un menu interactif s’affiche :

- **Acheter un domaine** : lance la procédure d’achat automatisée
- **Paramétrage** : configure les accès OVH, contacts, paiement, DNS…
- **Quitter** : sort du script

---

## Organisation du code

Le projet est organisé ainsi :

- `auto_domain.py` : script principal, point d'entrée, lance le menu et orchestre les fonctions
- `config_manager.py` : gestion de la configuration (lecture/écriture du fichier `config.json`)
- `domain.py` : validation du nom de domaine
- `util.py` : utilitaires CLI (saisie, choix, affichage, gestion erreurs)
- `config.json` : configuration persistante

### Responsabilités principales

- **auto_domain.py** : Point d’entrée du programme, boucle du menu interactif, logique d’achat et de paramétrage
- **config_manager.py** : Gère la lecture/écriture de la configuration dans `config.json`
- **domain.py** : Validation du format du nom de domaine
- **util.py** : Saisie utilisateur, choix dans une liste, affichage du panier, gestion des erreurs API

---

## Requêtes API OVH utilisées

Toutes les requêtes sont faites via la bibliothèque officielle `ovh`, qui gère l’authentification et la signature.

| Méthode | Endpoint | Description | Paramètres | Réponse attendue |
|---------|----------|-------------|------------|------------------|
| GET     | /me      | Vérifie la validité des clés API | Aucun | Infos du compte |
| GET     | /me/contact | Liste les contacts du compte | Aucun | Tableau d’ID de contacts |
| GET     | /me/contact/{id} | Détail d’un contact | id du contact | Infos du contact |
| GET     | /me/payment/method | Liste les moyens de paiement | Aucun | Tableau d’ID de moyens de paiement |
| GET     | /me/payment/method/{id} | Détail d’un moyen de paiement | id du moyen | Infos du moyen |
| POST    | /order/cart | Crée un panier | ovhSubsidiary, description | ID du panier |
| POST    | /order/cart/{cartId}/assign | Associe le panier à un NIC | nic | Confirmation |
| GET     | /order/cart/{cartId}/domain | Liste les offres pour un domaine | domain | Offres disponibles |
| POST    | /order/cart/{cartId}/domain | Ajoute un domaine au panier | domain, duration, planCode, pricingMode | ID de l’item |
| POST    | /order/cart/{cartId}/item/{itemId}/configuration | Configure un item (propriétaire, DNS…) | label, value | Confirmation |
| GET     | /order/cart/{cartId}/checkout | Récupère le récapitulatif du panier | Aucun | Détail du panier |
| POST    | /order/cart/{cartId}/checkout | Valide et paie la commande | paymentMethod | Confirmation, lien de paiement |

### Explications des paramètres principaux

- **ovhSubsidiary** : Filiale OVH (ex : FR, DE, ES…)
- **nic** : Identifiant client OVH (NIC handle)
- **domain** : Nom de domaine à acheter
- **duration** : Durée d’enregistrement (ex : P1Y pour 1 an)
- **planCode** : Code du plan d’offre (ex : domaine.fr)
- **pricingMode** : Mode de tarification (ex : default)
- **label/value** : Pour configurer l’item (OWNER_CONTACT, DOMAIN_DNS…)

---

## Comprendre les retours de l’API

- Toutes les réponses sont des objets ou tableaux JSON.
- Les erreurs sont capturées et affichées avec le code HTTP et un message explicite (voir `handle_api_error` dans `util.py`).
- Erreurs courantes : 400 (requête invalide), 401 (authentification), 403 (droit), 404 (ressource), 409 (conflit).

**Exemple de retour pour `/order/cart/{cartId}/checkout`** :

```json
{
  "items": [
    {
      "productId": "domain.fr",
      "prices": [
        {"label": "Total", "price": {"text": "12.00 €"}}
      ]
    }
  ],
  "prices": {
    "withTax": {"value": 12.00, "currencyCode": "EUR"}
  }
}
```

---

## Conseils pour les développeurs

- **Sécurité** : Ne partage jamais tes clés API, elles donnent accès à ton compte OVH.
- **Tests** : Utilise le mode "dry-run" (ne valide pas le paiement) pour tester sans acheter.
- **Logs** : Ajoute des impressions pour suivre les étapes si besoin.
- **Évolution** : Pour une vraie POO, tu pourrais encapsuler chaque fonctionnalité dans une classe (ConfigManager, OvhClient, etc.).

---

## Pour aller plus loin

- Créer ses propres tokens API OVH
- Exemples d’utilisation de l’API OVH en Python
- Documentation complète de chaque route : [API Console OVH](https://api.ovh.com/console/), [Guide général OVH API](https://docs.ovh.com/gb/en/api/first-steps-with-ovh-api/)

---

Ce README est conçu pour être un guide complet : il explique le but du projet, les prérequis, l’organisation, chaque fonction, chaque requête API, et donne des conseils pour comprendre et faire évoluer le code.

---

Create by Hugo Demangeat.
