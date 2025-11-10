from flask import Flask, render_template, json, request, redirect, url_for
import re

app = Flask(__name__)

# Function to load movie data from filmes.json
def carregar_filmes():
    try:
        with open('filmes.json', 'r', encoding='utf-8') as arquivo:
            data = json.load(arquivo)
            print("Conteúdo de 'filmes.json' carregado com sucesso.") # Debug print
            return data.get('filmes', [])
    except FileNotFoundError:
        print("Erro: O arquivo 'filmes.json' não foi encontrado. Certifique-se de que ele está na mesma pasta que 'app.py'.")
        return []
    except json.JSONDecodeError:
        print("Erro: O arquivo 'filmes.json' está mal formatado. Verifique a sintaxe JSON.")
        return []

# Load all movies once when the app starts
all_filmes = carregar_filmes()
print(f"Total de filmes carregados na inicialização: {len(all_filmes)}")
# Uncomment the line below to see all loaded movies (for extensive debugging)
# print(all_filmes)

# Rota for the home page (index.html)
@app.route('/')
def index():
    filmes = carregar_filmes()
    return render_template('index.html', filmes=filmes)

@app.route('/tudo')
def tudo():
    filmes = carregar_filmes()
    return render_template('tudo.html', filmes=filmes)
    return render_template('index.html', filmes=all_filmes)

# Rota for the all movies page (filmes.html)
@app.route('/filmes')
def filmes():
    return render_template('filmes.html', filmes=all_filmes)

# Rota for the genre listing page (generos.html)
@app.route('/generos')
def pagina_generos():
    # Define a fixed list of genres you want to display
    # 'Ficção' foi alterado para 'Ficção Científica'
    generos_desejados = [
        "Romance", "Comédia", "Terror", "Suspense", "Animação",
        "Ação", "Aventura", "Ficção Científica", "Drama", "Mistério", "Fantasia", # <-- ALTERADO AQUI
        "Documentário", "Musical"
    ]
    
    # Optional: You can still filter these based on what's actually in your movies.
    # For now, we'll just use the desired list directly.
    return render_template("generos.html", generos=sorted(generos_desejados))

# Rota to display movies of a specific genre
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

@app.route('/filme/<slug>')
def detalhes_filme(slug):
    filmes = carregar_filmes()
    filme = next((f for f in filmes if f['slug'] == slug), None)
    if filme:
        return render_template('detalhes.html', filme=filme)
    else:
        return "Filme não encontrado", 404

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
    # Filter movies where the genre (lowercase) is in the movie's genre list
    filmes_genero = [f for f in all_filmes if nome.lower() in [g.lower() for g in f.get("generos", [])]]
    
    # Debug prints for specific genre filtering
    print(f"Buscando filmes para o gênero: '{nome}'")
    print(f"Número de filmes encontrados para '{nome}': {len(filmes_genero)}")
    # Uncomment the line below to see the actual filtered movies (for extensive debugging)
    # print(filmes_genero)

    # Render the filmes_generos.html template with the genre and filtered movies
    return render_template("filmes_generos.html", genero=nome, filmes=filmes_genero)

# Entry point to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
