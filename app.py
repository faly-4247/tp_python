from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

taches = [
    {"id": 1, "titre": "Réviser les décorateurs",
     "priorite": "haute", "terminee": False},
    {"id": 2, "titre": "Installer Flask",
     "priorite": "normale", "terminee": True},
    {"id": 3, "titre": "Lire la documentation Jinja2",
     "priorite": "basse", "terminee": False},
]


@app.route("/")
def index():
    return render_template("taches.html", taches=taches)


@app.route("/taches/<int:id>")
def detail(id):
    for tache in taches:
        if tache["id"] == id:
            return render_template("detail.html", tache=tache)

    abort(404)

@app.route("/taches/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        priorite = request.form.get("priorite", "normale")

        if not titre:
            return render_template(
                "ajouter.html",
                erreur="Veuillez saisir un titre."
            )

        if len(titre) > 80:
            return render_template(
                "ajouter.html",
                erreur="Le titre ne doit pas dépasser 80 caractères."
            )

        if priorite not in ["basse", "normale", "haute"]:
            return render_template(
                "ajouter.html",
                erreur="Veuillez choisir une priorité valide."
            )

        nouvel_id = max(
            (t["id"] for t in taches),
            default=0
        ) + 1

        taches.append({
            "id": nouvel_id,
            "titre": titre,
            "priorite": priorite,
            "terminee": False
        })

        return redirect(url_for("index"))

    return render_template("ajouter.html")

if __name__ == "__main__":
    app.run(debug=True)
    