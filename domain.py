import re

def valider_nom_domaine(domain):
    motif = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$"
    return re.match(motif, domain) is not None
