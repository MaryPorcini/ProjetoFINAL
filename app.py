from flask import Flask, render_template, json, request, redirect, url_for
import re

app = Flask(__name__)

def carregar_filmes():
    try:
        with open('filmes.json', 'r', encoding='utf-8') as arquivo:
            data = json.load(arquivo)
            return data.get('filmes', [])
    except:
        return []

def criar_slug(texto):
    return re.sub(r'[^a-z0-9]+', '-', texto.lower()).strip('-')

all_filmes = carregar_filmes()

# Adiciona slug automaticamente se não existir
for f in all_filmes:
    if 'slug' not in f:
        f['slug'] = criar_slug(f['titulo'])

@app.route('/')
def index():
    return render_template('index.html', filmes=all_filmes)

@app.route('/filme/<slug>')
def detalhes_filme(slug):
    filme = next((f for f in all_filmes if f['slug'] == slug), None)
    if filme:
        return render_template('detalhes.html', filme=filme)
    return "Filme não encontrado", 404

@app.route('/tudo')
def tudo():
    filmes = carregar_filmes()
    return render_template('tudo.html', filmes=filmes)
    

@app.route('/filmes')
def filmes():
    return render_template('filmes.html', filmes=all_filmes)
    
@app.route('/generos')
def pagina_generos():
    generos_desejados = [
        "Romance", "Comédia", "Terror", "Suspense", "Animação",
        "Ação", "Aventura", "Ficção Científica", "Drama", "Mistério", "Fantasia", # <-- ALTERADO AQUI
        "Documentário", "Musical"
    ]
    
    return render_template("generos.html", generos=sorted(generos_desejados))

# Rota to display movies of a specific genre
@app.route("/generos/<nome>")
def filmes_do_genero(nome):
    # Filter movies where the genre (lowercase) is in the movie's genre list
    filmes_genero = [f for f in all_filmes if nome.lower() in [g.lower() for g in f.get("generos", [])]]
    
    # Debug prints for specific genre filtering
    print(f"Buscando filmes para o gênero: '{nome}'")
    print(f"Número de filmes encontrados para '{nome}': {len(filmes_genero)}")


    return render_template("filmes_generos.html", genero=nome, filmes=filmes_genero)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').lower()
    filmes = carregar_filmes()
    resultados = [f for f in filmes if termo in f['titulo'].lower()]
    return render_template('buscar.html', termo=termo, resultados=resultados)



@app.route('/personalizado')
def personalizado():
    filmes = carregar_filmes()
    return render_template('personalizado.html', filmes=filmes)

@app.route('/resultado_personalizado', methods=['POST'])
def resultado_personalizado():
    filmes = carregar_filmes()
    generos_selecionados = request.form.getlist('generos')
    ano_min = request.form.get('ano_min')
    ano_max = request.form.get('ano_max')
    avaliacao_min = request.form.get('avaliacao_min')

    filtrados = []
    for f in filmes:
        # Gêneros
        genero_ok = any(g in f['generos'] for g in generos_selecionados) if generos_selecionados else True
        
        # Ano de lançamento
        try:
            ano_lancamento = int(f['data_lancamento'].split('-')[0])
        except:
            ano_lancamento = 0  # ou continue se preferir ignorar filmes sem data válida

        ano_ok = True
        if ano_min and ano_lancamento < int(ano_min):
            ano_ok = False
        if ano_max and ano_lancamento > int(ano_max):
            ano_ok = False

        # Avaliação mínima
        avaliacao_ok = True
        if avaliacao_min:
            try:
                avaliacao_ok = f['avaliacao'] >= float(avaliacao_min)
            except:
                avaliacao_ok = False

        # Adiciona se passou em todos os filtros
        if genero_ok and ano_ok and avaliacao_ok:
            filtrados.append(f)

    return render_template('resultado_personalizado.html', filmes=filtrados)
    

# Entry point to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)