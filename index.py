from flask import Flask, request, jsonify

from service.ia_service import IAService
from core.prompt_mestre import PromptMestre


# Cria aplicação Flask
app = Flask(
    __name__,
    static_folder='static'
)

# Inicializa serviços
ia_service = IAService()
prompt_mestre = PromptMestre()


# Página inicial
@app.route('/')
def index():
    return app.send_static_file('index.html')


# CHAT
@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json.get('mensagem')

    if not user_message:
        return jsonify({
            'resposta': 'Por favor, forneça uma mensagem.'
        }), 400

    system_prompt = prompt_mestre.get_prompt()

    response = ia_service.enviar_mensagem(
        user_message,
        system_prompt
    )

    # 🚀 IMPORTANTE: não fazer mais replace aqui
    return jsonify({
        'resposta': response
    })


# NOVO CHAT
@app.route('/novo-chat')
def novo_chat():

    ia_service.historico = []

    return jsonify({
        "status": "novo chat iniciado"
    })


# AJUDA
@app.route('/ajuda')
def ajuda():

    return jsonify({
        "mensagem": "O FestaBot ajuda você a encontrar espaços para eventos."
    })


# CONFIGURAÇÕES
@app.route('/configuracoes')
def configuracoes():

    return jsonify({
        "tema": "claro",
        "modelo": "llama-3.3-70b-versatile"
    })


# Inicia servidor
if __name__ == '__main__':

    app.run(
        debug=True,
        port=5000
    )