from flask import Flask, render_template, json, request, redirect, url_for
import re

app = Flask(__name__)

# Função para carregar filmes do arquivo JSON e adicionar o slug
def carregar_filmes():
    with open('filmes.json', 'r', encoding='utf-8') as arquivo:
        filmes = json.load(arquivo)['filmes']
        for f in filmes:
            f['avaliacao'] = float(f['avaliacao'])  # garante que avaliação é número
            # cria slug a partir do título (ex: "A Bruxa" -> "a-bruxa")
            f['slug'] = re.sub(r'[^a-z0-9]+', '-', f['titulo'].lower()).strip('-')
        return filmes

@app.route('/')
def index():
    filmes = carregar_filmes()
    return render_template('index.html', filmes=filmes)

@app.route('/tudo')
def tudo():
    filmes = carregar_filmes()
    return render_template('tudo.html', filmes=filmes)

@app.route('/generos')
def pagina_generos():
    generos = [
        "Ficção", "Ação", "Aventura", "Romance", "Comédia", "Dorama", "Animação",
        "Drama", "Terror", "Mistério", "Suspense", "Musical", "Fantasia", "Documentário"
    ]
    return render_template("generos.html", generos=generos)

@app.route("/generos/<nome>")
def filmes_do_genero(nome):
    filmes = carregar_filmes()
    filmes_genero = [f for f in filmes if nome.lower() in [g.lower() for g in f["generos"]]]
    return render_template("filmes_genero.html", genero=nome, filmes=filmes_genero)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').lower()
    filmes = carregar_filmes()
    resultados = [f for f in filmes if termo in f['titulo'].lower()]
    return render_template('buscar.html', termo=termo, resultados=resultados)

# NOVA ROTA PARA DETALHES DO FILME
@app.route('/filme/<slug>')
def detalhes_filme(slug):
    filmes = carregar_filmes()
    filme = next((f for f in filmes if f['slug'] == slug), None)
    if filme:
        return render_template('detalhes.html', filme=filme)
    else:
        return "Filme não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
