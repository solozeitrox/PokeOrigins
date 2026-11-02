
from flask import Flask, render_template

app = Flask(__name__)

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

# Badges actuellement obtenus par le joueur.
# À connecter plus tard au système de comptes.
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
        progression_arenes=progression_arenes
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
