from flask import Flask, render_template, json, request, redirect, url_for
import re

app = Flask(__name__)

# Função para carregar filmes do arquivo JSON e adicionar o slug
def carregar_filmes():
    with open('filmes.json', 'r', encoding='utf-8') as arquivo:
        filmes = json.load(arquivo)['filmes']
        for f in filmes:
            f['avaliacao'] = float(f['avaliacao'])  # garante que avaliação é número
            f['slug'] = re.sub(r'[^a-z0-9]+', '-', f['titulo'].lower()).strip('-')  # cria slug
        return filmes

@app.route('/')
def index():
    filmes = carregar_filmes()
    return render_template('index.html', filmes=filmes)

@app.route('/tudo')
def tudo():
    filmes = carregar_filmes()
    return render_template('tudo.html', filmes=filmes)


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

if __name__ == '__main__':
    app.run(debug=True)
