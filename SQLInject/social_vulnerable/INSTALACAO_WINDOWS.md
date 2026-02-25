# 🪟 Guia de Instalação para Windows - Social Vulnerable

Este guia mostra como instalar e executar o projeto no **Windows** usando **SQLite3** (sem necessidade de MySQL).

## ✅ Vantagens do SQLite3

- ✅ Funciona nativamente no Windows
- ✅ Sem necessidade de instalar MySQL
- ✅ Sem problemas com `mysqlclient`
- ✅ Arquivo único de banco de dados (`db.sqlite3`)
- ✅ Perfeito para fins educacionais
- ✅ Mantém todas as vulnerabilidades de SQL Injection

---

## 🚀 Instalação em 3 Passos

### Passo 1: Instalar Python e Dependências

**1. Verificar Python instalado:**
```bash
python --version
```

Se não tiver Python, baixe em: https://www.python.org/downloads/

**2. Instalar Django:**
```bash
pip install django
```

### Passo 2: Preparar o Banco de Dados

**1. Navegar até a pasta do projeto:**
```bash
cd C:\caminho\para\social_vulnerable
```

**2. Executar migrações (cria o banco SQLite3):**
```bash
python manage.py migrate
```

Você verá:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, social
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying social.0001_initial... OK
```

### Passo 3: Iniciar o Servidor

```bash
python manage.py runserver
```

Você verá:
```
Watching for file changes with StatReloader
Quit the server with CONTROL-C.
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Acessar a Aplicação

Abra seu navegador e vá para:

| Página | URL |
|--------|-----|
| **Cadastro** | http://localhost:8000/register/ |
| **Login** | http://localhost:8000/login/ |
| **Feed** | http://localhost:8000/feed/ |
| **Buscar** | http://localhost:8000/search/ |
| **Perfil** | http://localhost:8000/profile/username/ |

---

## 🧪 Testar SQL Injection

### 1. Criar uma Conta

1. Acesse: http://localhost:8000/register/
2. Preencha:
   - Username: `alice`
   - Email: `alice@example.com`
   - Password: `senha123`
   - Bio: `Olá, sou Alice!`
3. Clique em "Cadastrar"

### 2. Fazer Login

1. Acesse: http://localhost:8000/login/
2. Preencha:
   - Username: `alice`
   - Password: `senha123`
3. Clique em "Entrar"

### 3. Testar SQL Injection na Busca

1. Acesse: http://localhost:8000/search/
2. Digite na busca: `%' OR '1'='1`
3. Clique em "Buscar"
4. **Resultado**: Retorna todos os usuários!

### 4. Testar SQL Injection no Perfil

1. Acesse: http://localhost:8000/profile/alice%27%20OR%20%271%27=%271%20--/
2. **Resultado**: Retorna o perfil do primeiro usuário

---

## 📊 Estrutura do Banco de Dados

O SQLite3 cria um arquivo `db.sqlite3` com as seguintes tabelas:

```
db.sqlite3
├── users (id, username, password, email, bio, created_at, updated_at)
├── posts (id, user_id, content, created_at, updated_at)
└── follows (id, follower_id, following_id, created_at)
```

---

## 🔧 Configuração do SQLite3

O arquivo `social_config/settings.py` já está configurado para SQLite3:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Não precisa mudar nada!**

---

## 🛑 Parar o Servidor

Pressione `CTRL + C` no terminal onde o servidor está rodando.

---

## 🔄 Reiniciar o Servidor

```bash
python manage.py runserver
```

---

## 📁 Estrutura do Projeto

```
social_vulnerable/
├── social_config/
│   ├── settings.py          # Configurações (SQLite3)
│   ├── urls.py
│   └── wsgi.py
├── social/
│   ├── models.py            # Modelos (User, Post, Follow)
│   ├── views.py             # Views com SQL Injection
│   ├── urls.py
│   └── templates/
│       └── social/
│           ├── base.html
│           ├── login.html
│           ├── register.html
│           ├── feed.html
│           ├── profile.html
│           └── search.html
├── manage.py
├── db.sqlite3               # Banco de dados (criado automaticamente)
└── README_ATUALIZADO.md
```

---

## 🐛 Troubleshooting

### ❌ Erro: "ModuleNotFoundError: No module named 'django'"

**Solução:**
```bash
pip install django
```

### ❌ Erro: "Port 8000 already in use"

**Solução - Usar porta diferente:**
```bash
python manage.py runserver 8001
```

Depois acesse: http://localhost:8001

### ❌ Erro: "No such table: social_users"

**Solução - Executar migrações:**
```bash
python manage.py migrate
```

### ❌ Página em branco ou erro 404

**Solução:**
1. Certifique-se de que o servidor está rodando
2. Verifique a URL (deve ser exatamente como nos exemplos)
3. Recarregue a página (F5)

---

## 📚 Documentação

- **README_ATUALIZADO.md** - Documentação completa
- **PAYLOADS_BUSCA_FOLLOW.md** - Exemplos de SQL Injection
- **PAYLOADS.md** - Payloads adicionais

---

## 💡 Dicas para Windows

1. **Use PowerShell ou CMD**: Ambos funcionam bem
2. **Caminho com espaços**: Use aspas se o caminho tiver espaços
   ```bash
   cd "C:\Users\Seu Nome\Documentos\social_vulnerable"
   ```
3. **Atalho para abrir PowerShell**: Shift + Clique direito na pasta
4. **Recarregar página**: F5 no navegador

---

## 🎓 Próximos Passos

1. Crie várias contas de teste
2. Teste os payloads de SQL Injection
3. Estude como as vulnerabilidades funcionam
4. Aprenda como proteger aplicações
5. Use em sua aula sobre segurança!

---

## 📞 Suporte

Para dúvidas:
- **Django**: https://docs.djangoproject.com
- **SQLite3**: https://www.sqlite.org
- **SQL Injection**: https://owasp.org/www-community/attacks/SQL_Injection

---

**Pronto! Agora você pode usar o Social Vulnerable no Windows! 🎉**
