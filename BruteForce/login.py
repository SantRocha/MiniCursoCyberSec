from flask import Flask, request

app = Flask(__name__)

@app.route('/login/', methods=['POST', 'GET'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if email != 'admin@hermes.com':
            return 'Erro: Usuário não existe', 401
        
        if senha != 'senha123':
            return 'Erro: Senha incorreta', 401
            
        return 'Sucesso: Bem-vindo ao painel do Hermes 2025!', 200
    
    return 'Envie um POST com email e senha.'

if __name__ == '__main__':
    print("🚀 Servidor de testes do Hermes 2025 rodando...")
    print("Acesse: http://127.0.0.1:8000/login/")
    app.run(host='0.0.0.0', port=8000)