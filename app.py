
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os
import hashlib

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================

FUSEAU_HORAIRE = ZoneInfo("Europe/Paris")
FICHIER_QUETES = "quetes_data.json"

# À configurer avant de connecter publiquement
# le serveur Minecraft à cette API.
CLE_API = os.environ.get("POKEORIGINS_API_KEY")


def date_actuelle():
    return datetime.now(FUSEAU_HORAIRE).date().isoformat()


def semaine_actuelle():
    return datetime.now(FUSEAU_HORAIRE).strftime("%G-W%V")


# ==========================================
# QUETES QUOTIDIENNES
# ==========================================

QUETES_QUOTIDIENNES = [
    {
        "id": "capture_daily",
        "nom": "Petit collectionneur",
        "description": "Capturer 3 Pokémon.",
        "evenement": "capture",
        "objectif": 3,
        "xp": 20
    },
    {
        "id": "combat_daily",
        "nom": "Combattant du jour",
        "description": "Gagner 2 combats Pokémon.",
        "evenement": "combat",
        "objectif": 2,
        "xp": 30
    },
    {
        "id": "exploration_daily",
        "nom": "Explorateur",
        "description": "Explorer 1 biome.",
        "evenement": "biome",
        "objectif": 1,
        "xp": 50
    }
]


# ==========================================
# CATALOGUE DES QUETES HEBDOMADAIRES
# ==========================================

CATALOGUE_HEBDOMADAIRE = [
    {
        "id": "capture_week",
        "nom": "Grand collectionneur",
        "description": "Capturer 40 Pokémon.",
        "evenement": "capture",
        "objectif": 40,
        "xp": 120
    },
    {
        "id": "combat_week",
        "nom": "Combattant expérimenté",
        "description": "Gagner 15 combats.",
        "evenement": "combat",
        "objectif": 15,
        "xp": 120
    },
    {
        "id": "raid_week",
        "nom": "Chasseur de raids",
        "description": "Participer à 5 raids.",
        "evenement": "raid",
        "objectif": 5,
        "xp": 120
    },
    {
        "id": "trainer_week",
        "nom": "Dresseur redoutable",
        "description": "Vaincre 10 dresseurs.",
        "evenement": "trainer",
        "objectif": 10,
        "xp": 120
    },
    {
        "id": "biome_week",
        "nom": "Grand explorateur",
        "description": "Explorer 3 biomes différents.",
        "evenement": "biome",
        "objectif": 3,
        "xp": 120
    },
    {
        "id": "evolution_week",
        "nom": "Maître de l'évolution",
        "description": "Faire évoluer 5 Pokémon.",
        "evenement": "evolution",
        "objectif": 5,
        "xp": 120
    },
    {
        "id": "trade_week",
        "nom": "Marchand Pokémon",
        "description": "Effectuer 3 échanges au GTS.",
        "evenement": "trade",
        "objectif": 3,
        "xp": 120
    },
    {
        "id": "distance_week",
        "nom": "Voyageur",
        "description": "Parcourir 5 000 blocs.",
        "evenement": "blocks",
        "objectif": 5000,
        "xp": 120
    }
]


# ==========================================
# SAUVEGARDE DES QUETES
# ==========================================

def charger_donnees_quetes():

    if not os.path.exists(FICHIER_QUETES):
        return {}

    try:
        with open(FICHIER_QUETES, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_donnees_quetes(donnees):

    with open(FICHIER_QUETES, "w", encoding="utf-8") as fichier:
        json.dump(
            donnees,
            fichier,
            indent=4,
            ensure_ascii=False
        )


def creer_etat_quetes():

    return {
        "date": date_actuelle(),
        "semaine": semaine_actuelle(),
        "progression": {},
        "recompenses": [],
        "xp_battlepass": 0
    }


def obtenir_etat_quetes():

    donnees = charger_donnees_quetes()

    if "joueur_demo" not in donnees:
        donnees["joueur_demo"] = creer_etat_quetes()

    etat = donnees["joueur_demo"]

    # Réinitialisation quotidienne
    if etat.get("date") != date_actuelle():

        etat["date"] = date_actuelle()

        for quete in QUETES_QUOTIDIENNES:
            etat["progression"].pop(quete["id"], None)
            etat["recompenses"] = [
                r for r in etat["recompenses"]
                if r != quete["id"]
            ]

    # Réinitialisation hebdomadaire
    if etat.get("semaine") != semaine_actuelle():

        etat["semaine"] = semaine_actuelle()

        for quete in CATALOGUE_HEBDOMADAIRE:
            etat["progression"].pop(quete["id"], None)
            etat["recompenses"] = [
                r for r in etat["recompenses"]
                if r != quete["id"]
            ]

    sauvegarder_donnees_quetes(donnees)

    return etat


# ==========================================
# SELECTION DES 5 QUETES HEBDOMADAIRES
# ==========================================

def obtenir_quetes_hebdomadaires():

    numero_semaine = datetime.now(FUSEAU_HORAIRE).isocalendar().week

    debut = (numero_semaine * 5) % len(CATALOGUE_HEBDOMADAIRE)

    catalogue = CATALOGUE_HEBDOMADAIRE

    return [
        catalogue[(debut + i) % len(catalogue)].copy()
        for i in range(5)
    ]


# ==========================================
# PROGRESSION AUTOMATIQUE
# ==========================================

def enregistrer_evenement(evenement, quantite=1):

    if not isinstance(quantite, int) or quantite < 1:
        return False

    etat = obtenir_etat_quetes()

    toutes_les_quetes = (
        QUETES_QUOTIDIENNES
        + obtenir_quetes_hebdomadaires()
    )

    for quete in toutes_les_quetes:

        if quete["evenement"] != evenement:
            continue

        identifiant = quete["id"]

        if identifiant in etat["recompenses"]:
            continue

        progression = etat["progression"].get(identifiant, 0)

        progression = min(
            progression + quantite,
            quete["objectif"]
        )

        etat["progression"][identifiant] = progression

        # Récompense automatique une seule fois
        if progression >= quete["objectif"]:

            etat["recompenses"].append(identifiant)

            etat["xp_battlepass"] += quete["xp"]

    donnees = charger_donnees_quetes()
    donnees["joueur_demo"] = etat
    sauvegarder_donnees_quetes(donnees)

    return True


# ==========================================
# AFFICHAGE DES QUETES
# ==========================================

def preparer_quetes(quetes, etat):

    resultat = []

    for quete in quetes:

        copie = quete.copy()

        identifiant = copie["id"]

        progression = etat["progression"].get(identifiant, 0)

        copie["progression"] = progression

        copie["terminee"] = (
            progression >= copie["objectif"]
        )

        copie["reclamee"] = (
            identifiant in etat["recompenses"]
        )

        copie["pourcentage"] = round(
            progression / copie["objectif"] * 100
        )

        resultat.append(copie)

    return resultat


def obtenir_resume_quetes():

    etat = obtenir_etat_quetes()

    quotidiennes = preparer_quetes(
        QUETES_QUOTIDIENNES,
        etat
    )

    hebdomadaires = preparer_quetes(
        obtenir_quetes_hebdomadaires(),
        etat
    )

    return {
        "quotidiennes": quotidiennes,
        "hebdomadaires": hebdomadaires,
        "xp_battlepass": etat["xp_battlepass"],
        "xp_quotidienne": sum(
            q["xp"] for q in QUETES_QUOTIDIENNES
        ),
        "xp_hebdomadaire": 600,
        "quotidiennes_terminees": sum(
            q["terminee"] for q in quotidiennes
        ),
        "hebdomadaires_terminees": sum(
            q["terminee"] for q in hebdomadaires
        )
    }


# ==========================================
# PAGE DES QUETES
# ==========================================

@app.route("/quetes")
def quetes():

    progression = obtenir_resume_quetes()

    return render_template(
        "quetes.html",
        progression=progression,
        quetes_quotidiennes=progression["quotidiennes"],
        quetes_hebdomadaires=progression["hebdomadaires"]
    )


# ==========================================
# API DE PROGRESSION MINECRAFT
# ==========================================

@app.route("/api/quetes/progression", methods=["POST"])
def api_progression_quetes():

    # Protection obligatoire de l'API
    if not CLE_API:
        return jsonify({
            "succes": False,
            "erreur": "API non configurée."
        }), 503

    cle = request.headers.get("X-API-Key")

    if cle != CLE_API:
        return jsonify({
            "succes": False,
            "erreur": "Accès refusé."
        }), 401

    donnees = request.get_json(silent=True) or {}

    evenement = donnees.get("evenement")
    quantite = donnees.get("quantite", 1)

    evenements_autorises = [
        "capture",
        "combat",
        "raid",
        "trainer",
        "biome",
        "evolution",
        "trade",
        "blocks"
    ]

    if evenement not in evenements_autorises:
        return jsonify({
            "succes": False,
            "erreur": "Événement inconnu."
        }), 400

    if (
        not isinstance(quantite, int)
        or isinstance(quantite, bool)
        or quantite < 1
        or quantite > 100000
    ):
        return jsonify({
            "succes": False,
            "erreur": "Quantité invalide."
        }), 400

    enregistrer_evenement(evenement, quantite)

    return jsonify({
        "succes": True,
        "progression": obtenir_resume_quetes()
    })


# ==========================================
# SYSTÈME DES 8 ARÈNES POKEORIGINS
# ==========================================

ARENES = [
    {
        "id": 1,
        "nom": "Arène Flora",
        "champion": "Champion Flora",
        "type": "Plante",
        "niveau": 15,
        "badge": "Badge Flora",
        "couleur": "#55c878",
        "theme": "Forêt enchantée",
        "description": "Une arène entourée de végétation, de fleurs et de plantes sauvages.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": True,
        "terminee": False
    },
    {
        "id": 2,
        "nom": "Arène Néo",
        "champion": "Champion Néo",
        "type": "Eau",
        "niveau": 25,
        "badge": "Badge Néo",
        "couleur": "#38a9ed",
        "theme": "Palais aquatique",
        "description": "Un gymnase aquatique composé de bassins et de cascades.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    },
    {
        "id": 3,
        "nom": "Arène Volt",
        "champion": "Champion Volt",
        "type": "Électrik",
        "niveau": 35,
        "badge": "Badge Volt",
        "couleur": "#f4d342",
        "theme": "Centrale électrique",
        "description": "Une arène technologique alimentée par une puissante énergie électrique.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    },
    {
        "id": 4,
        "nom": "Arène Kael",
        "champion": "Champion Kael",
        "type": "Feu",
        "niveau": 45,
        "badge": "Badge Kael",
        "couleur": "#f07838",
        "theme": "Volcan",
        "description": "Un gymnase construit au cœur d'un environnement volcanique.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    },
    {
        "id": 5,
        "nom": "Arène Nyx",
        "champion": "Champion Nyx",
        "type": "Spectre",
        "niveau": 60,
        "badge": "Badge Nyx",
        "couleur": "#9865cf",
        "theme": "Manoir hanté",
        "description": "Un mystérieux manoir plongé dans l'obscurité.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    },
    {
        "id": 6,
        "nom": "Arène Yuki",
        "champion": "Champion Yuki",
        "type": "Glace",
        "niveau": 70,
        "badge": "Badge Yuki",
        "couleur": "#76d9ee",
        "theme": "Palais de glace",
        "description": "Un palais entièrement recouvert de glace et de cristaux.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    },
    {
        "id": 7,
        "nom": "Arène Astra",
        "champion": "Champion Astra",
        "type": "Psy",
        "niveau": 85,
        "badge": "Badge Astra",
        "couleur": "#d477d9",
        "theme": "Temple cosmique",
        "description": "Un gymnase mystérieux inspiré de l'espace et des pouvoirs psychiques.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    },
    {
        "id": 8,
        "nom": "Arène Ryū",
        "champion": "Champion Ryū",
        "type": "Dragon",
        "niveau": 100,
        "badge": "Badge Ryū",
        "couleur": "#e45b70",
        "theme": "Sanctuaire des dragons",
        "description": "L'ultime gymnase, réservé aux meilleurs dresseurs.",
        "equipe": ["À définir"] * 6,
        "image": "",
        "badge_image": "",
        "debloquee": False,
        "terminee": False
    }
]

BADGES_OBTENUS = []


def obtenir_progression_arenes():

    progression = len(BADGES_OBTENUS)

    arenes = []

    for arene in ARENES:

        arene_copie = arene.copy()

        arene_copie["terminee"] = (
            arene["id"] in BADGES_OBTENUS
        )

        arene_copie["debloquee"] = (
            arene["id"] == 1
            or arene["id"] - 1 in BADGES_OBTENUS
        )

        arenes.append(arene_copie)

    return {
        "arenes": arenes,
        "badges_obtenus": progression,
        "total_badges": 8,
        "pourcentage": round(progression / 8 * 100),
        "terminee": progression == 8
    }


# ==========================================
# ACCUEIL
# ==========================================

@app.route("/")
def accueil():
    return render_template("index.html")


# ==========================================
# PRESENTATION
# ==========================================

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")


# ==========================================
# JOUEUR
# ==========================================

@app.route("/joueur")
def joueur():

    minecraft_lie = False

    progression_arenes = obtenir_progression_arenes()
    progression_quetes = obtenir_resume_quetes()

    informations_joueur = {
        "pseudo": "Non connecté",
        "minecraft_lie": minecraft_lie,
        "pseudo_minecraft": "Non connecté",
        "niveau": 0,
        "xp": 0,
        "xp_suivant": 0,
        "progression_xp": 0
    }

    statistiques = {
        "captures": 0,
        "decouverts": 0,
        "combats": 0,
        "victoires": 0,
        "champions": progression_arenes["badges_obtenus"],
        "argent": 0,
        "badges": progression_arenes["badges_obtenus"],
        "temps_jeu": "0h"
    }

    pokemons = []

    pokedex = {
        "captures": 0,
        "total": 1025,
        "pourcentage": 0
    }

    return render_template(
        "joueur.html",
        joueur=informations_joueur,
        stats=statistiques,
        pokemons=pokemons,
        pokedex=pokedex,
        progression_arenes=progression_arenes,
        progression_quetes=progression_quetes
    )


# ==========================================
# POKEDEX PERSONNEL
# ==========================================

@app.route("/pokedex")
def pokedex_joueur():

    pokemons = [
        {
            "numero": 1,
            "nom": "Bulbizarre",
            "decouvert": True,
            "capture": True,
            "image": "",
            "types": ["Plante", "Poison"]
        },
        {
            "numero": 4,
            "nom": "Salamèche",
            "decouvert": True,
            "capture": True,
            "image": "",
            "types": ["Feu"]
        },
        {
            "numero": 7,
            "nom": "Carapuce",
            "decouvert": True,
            "capture": False,
            "image": "",
            "types": ["Eau"]
        },
        {
            "numero": 25,
            "nom": "Pikachu",
            "decouvert": True,
            "capture": False,
            "image": "",
            "types": ["Électrik"]
        },
        {
            "numero": 6,
            "nom": "Dracaufeu",
            "decouvert": False,
            "capture": False,
            "image": "",
            "types": ["Feu", "Vol"]
        }
    ]

    total_pokemons = 1025

    captures = sum(1 for p in pokemons if p["capture"])

    pokedex = {
        "captures": captures,
        "total": total_pokemons,
        "pourcentage": round(captures / total_pokemons * 100, 1)
    }

    types_pokemon = [
        "Normal", "Feu", "Eau", "Plante", "Électrik",
        "Glace", "Combat", "Poison", "Sol", "Vol",
        "Psy", "Insecte", "Roche", "Spectre",
        "Dragon", "Ténèbres", "Acier", "Fée"
    ]

    return render_template(
        "pokedex_joueur.html",
        pokedex=pokedex,
        pokemons=pokemons,
        types_pokemon=types_pokemon,
        minecraft_lie=False
    )


# ==========================================
# WIKI
# ==========================================

@app.route("/wiki")
def wiki():
    return render_template("wiki.html")


@app.route("/wiki/pokedex")
def wiki_pokedex():
    return render_template("pokedex.html")


@app.route("/wiki/commandes")
def wiki_commandes():
    return render_template("commandes.html")


@app.route("/wiki/guides")
def wiki_guides():
    return render_template("guides.html")


@app.route("/wiki/economie")
def wiki_economie():
    return render_template("economie.html")


@app.route("/wiki/reglement")
def wiki_reglement():
    return render_template("reglement.html")

@app.route("/quetes")
def quetes():
    progression, quetes_quotidiennes, quetes_hebdomadaires = obtenir_resume_quetes()
    return render_template(
        "quetes.html",
        progression=progression,
        quetes_quotidiennes=quetes_quotidiennes,
        quetes_hebdomadaires=quetes_hebdomadaires
    )


# ==========================================
# ARENES POKEORIGINS
# ==========================================

@app.route("/wiki/arenes")
def wiki_arenes():

    progression = obtenir_progression_arenes()

    return render_template(
        "arenes.html",
        arenes=progression["arenes"],
        progression_arenes=progression
    )


# ==========================================
# AUTRES PAGES
# ==========================================

@app.route("/vote")
def vote():
    return render_template("vote.html")


@app.route("/boutique")
def boutique():
    return render_template("boutique.html")


@app.route("/actualites")
def actualites():
    return render_template("actualites.html")


@app.route("/classements")
def classements():
    return render_template("classements.html")


@app.route("/discord")
def discord():
    return render_template("discord.html")


# ==========================================
# LANCEMENT
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
