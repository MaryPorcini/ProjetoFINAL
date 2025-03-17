from flask import Flask, render_template, json

app = Flask(__name__)

def carregar_filmes():
    with open('filmes.json', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)['filmes']

@app.route('/')
def index():
    filmes = carregar_filmes()
    return render_template('index.html', filmes=filmes)

if __name__ == '_main_':
    app.run(debug=True)