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
# ESPACE JOUEUR
# ==============================

@app.route("/joueur")
def joueur():
    return render_template(
        "joueur.html",
        joueur=None,
        stats=None
    )


# ==============================
# POKEDEX PERSONNEL
# ==============================

@app.route("/pokedex")
def pokedex_joueur():
    return render_template(
        "pokedex_joueur.html",
        pokedex=None,
        pokemons=[],
        types_pokemon=[],
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