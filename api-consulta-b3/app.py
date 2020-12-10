from flask import Flask, request, jsonify
from yahooquery import Ticker
from datetime import datetime
import pytz
import random
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return "API para gerar valores de ações do B3."


@app.route('/acoes/<codigo_acao>', methods=['GET'])
def gerar_valor_acao(codigo_acao):
    ticker_acao = Ticker(codigo_acao)
    resultado = ticker_acao.history(period="7d",  interval="5m")
    resultado.reset_index(inplace=True)

    index = random.randrange(0, resultado.shape[0], 1)
    resultado = resultado.iloc[[index]]

    retorno = {'codigo': codigo_acao,
               'horario': datetime.now(pytz.timezone('AMERICA/Sao_Paulo')).isoformat(),
               'valor': resultado['close'].values[0]}

    return retorno, 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
