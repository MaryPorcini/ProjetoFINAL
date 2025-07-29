from flask import Flask, render_template, json

app = Flask(__name__)

# Function to load movie data from filmes.json
def carregar_filmes():
    try:
        with open('filmes.json', 'r', encoding='utf-8') as arquivo:
            data = json.load(arquivo)
            return data.get('filmes', [])
    except FileNotFoundError:
        print("Erro: O arquivo 'filmes.json' não foi encontrado. Certifique-se de que ele está na mesma pasta que 'app.py'.")
        return []
    except json.JSONDecodeError:
        print("Erro: O arquivo 'filmes.json' está mal formatado. Verifique a sintaxe JSON.")
        return []

# Load all movies once when the app starts
all_filmes = carregar_filmes()

# Rota for the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html', filmes=all_filmes)

# Rota for the all movies page (filmes.html)
@app.route('/filmes')
def filmes():
    return render_template('filmes.html', filmes=all_filmes)

# Rota for the genre listing page (generos.html)
@app.route('/generos')
def pagina_generos():
    # Define a fixed list of genres you want to display
    generos_desejados = [
        "Romance", "Comédia", "Terror", "Suspense", "Dorama", "Animação",
        "Ação", "Aventura", "Ficção", "Drama", "Mistério", "Fantasia",
        "Documentário", "Musical"
    ]
    
    # Optional: You can still filter these based on what's actually in your movies.
    # For now, we'll just use the desired list directly.
    return render_template("generos.html", generos=sorted(generos_desejados))

# Rota to display movies of a specific genre
@app.route("/generos/<nome>")
def filmes_do_genero(nome):
    # Filter movies where the genre (lowercase) is in the movie's genre list
    filmes_genero = [f for f in all_filmes if nome.lower() in [g.lower() for g in f.get("generos", [])]]

    # Render the filmes_generos.html template with the genre and filtered movies
    return render_template("filmes_generos.html", genero=nome, filmes=filmes_genero)

# Entry point to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)