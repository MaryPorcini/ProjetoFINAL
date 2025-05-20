from flask import Flask, render_template, json

app = Flask(__name__)

def carregar_filmes():
    with open('filmes.json', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)['filmes']

@app.route('/')
def index():
    filmes = carregar_filmes()
    return render_template('index.html', filmes=filmes)


@app.route('/filmes')
def filmes():
    filmes = carregar_filmes()
    return render_template('filmes.html', filmes=filmes)



@app.route("/generos")
def pagina_generos():
    generos = [
        "Ficção", "Ação", "Aventura", "Romance", "Comédia", "Dorama", "Animação",
        "Drama", "Terror", "Mistério", "Suspense", "Musical", "Fantasia", "Documentário"
    ]
    return render_template("generos.html", generos=generos)

@app.route("/generos/<nome>")
def filmes_do_genero(nome):
    filmes = carregar_filmes()
    filmes_genero = [f for f in filmes if f["genero"].lower() == nome.lower()]

    return render_template("filmes_genero.html", genero=nome, filmes=filmes_genero)


if __name__ == '__main__':
    app.run(debug=True)