from flask import Flask, render_template

app = Flask(__name__)

# ==============================
# ACCUEIL
# ==============================

@app.route("/")
def accueil():
    return render_template("index.html")


# ==============================
# PRESENTATION
# ==============================

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")


# ==============================
# JOUEUR
# ==============================

@app.route("/joueur")
def joueur():

    # Pour le moment, aucun compte Minecraft n'est réellement connecté.
    minecraft_lie = False

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
        "champions": 0,
        "argent": 0,
        "badges": 0,
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
        pokedex=pokedex
    )


# ==============================
# POKEDEX PERSONNEL
# ==============================

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


# ==============================
# WIKI
# ==============================

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


@app.route("/wiki/arenes")
def wiki_arenes():
    return render_template("arenes.html")


# ==============================
# AUTRES PAGES
# ==============================

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


# ==============================
# LANCEMENT
# ==============================

if __name__ == "__main__":
    app.run(debug=True)