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

    informations_joueur = {
        "pseudo": "Aventurier",
        "minecraft_lie": False,
        "pseudo_minecraft": "Non connecté",
        "niveau": 12,
        "xp": 750,
        "xp_suivant": 1000,
        "progression_xp": 75
    }

    statistiques = {
        "captures": 24,
        "decouverts": 56,
        "combats": 38,
        "victoires": 29,
        "champions": 2,
        "argent": 12500,
        "badges": 2,
        "temps_jeu": "12h 35min"
    }

    return render_template(
        "joueur.html",
        joueur=informations_joueur,
        stats=statistiques
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

    total_pokemons = 151
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