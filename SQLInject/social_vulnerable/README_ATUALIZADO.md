# Social Vulnerable - Rede Social com SQL Injection (Atualizado)

Uma aplicação web educacional desenvolvida em **Django** com **MySQL**, propositalmente vulnerável a ataques de **SQL Injection** para fins de ensino e demonstração de segurança.

## 🆕 Novas Funcionalidades (v2.0)

### ✨ Sistema de Busca de Usuários
- Busca por username ou email
- **Vulnerável a SQL Injection** no parâmetro de busca
- Testes: `%' OR '1'='1`, `UNION SELECT`, `SLEEP(5)`

### 👥 Sistema de Follow/Unfollow
- Siga outros usuários como Twitter/Instagram
- **Vulnerável a SQL Injection** nas operações de follow
- Feed inteligente com postagens destacadas

### 📱 Feed Inteligente
- Postagens de quem você segue aparecem no topo (destacadas)
- Postagens de outros usuários aparecem abaixo
- Atualização em tempo real

### 👤 Perfil Aprimorado
- Exibe estatísticas (seguidores, seguindo, postagens)
- Botões de follow/unfollow
- **Vulnerável a SQL Injection** na URL do perfil

---

## 🎯 Funcionalidades Existentes

### Autenticação (Vulnerável)
- **Cadastro de usuários**: Formulário para criar nova conta com SQL Injection
- **Login**: Sistema de autenticação vulnerável a bypass
- **Logout**: Encerrar sessão do usuário

### Feed Social
- **Página principal**: Exibe postagens com priorização de seguidos
- **Criar postagens**: Publicar textos para outros usuários verem
- **Perfil de usuário**: Visualizar informações e postagens de qualquer usuário

### Interface
- Design elegante com gradiente roxo
- Responsivo para dispositivos móveis
- Estilos CSS inline para facilitar modificações

---

## 🏗️ Arquitetura

```
social_vulnerable/
├── social_config/          # Configurações Django
│   ├── settings.py        # Configurações (MySQL, apps, etc)
│   ├── urls.py            # Rotas principais
│   └── wsgi.py
├── social/                 # Aplicação principal
│   ├── models.py          # Modelos (User, Post, Follow)
│   ├── views.py           # Views com SQL Injection
│   ├── urls.py            # Rotas da aplicação
│   └── templates/
│       └── social/
│           ├── base.html      # Template base
│           ├── login.html     # Página de login
│           ├── register.html  # Página de cadastro
│           ├── feed.html      # Feed de postagens
│           ├── profile.html   # Perfil do usuário
│           └── search.html    # Busca de usuários
├── manage.py              # Gerenciador Django
├── README.md              # Este arquivo
├── PAYLOADS.md            # Payloads SQL Injection (original)
├── PAYLOADS_BUSCA_FOLLOW.md # Payloads para busca e follow
└── QUICK_START.md         # Guia rápido de instalação
```

---

## 📊 Banco de Dados

### Tabela: users
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Tabela: posts
```sql
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Tabela: follows (NOVA)
```sql
CREATE TABLE follows (
    id INT PRIMARY KEY AUTO_INCREMENT,
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_follow (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 🔓 Vulnerabilidades Implementadas

### 1. SQL Injection no Login
**Localização**: `social/views.py` - função `login()`
**Tipo**: Autenticação Bypass
**Payload**: `admin' --`

### 2. SQL Injection no Cadastro
**Localização**: `social/views.py` - função `register()`
**Tipo**: Stacked Queries
**Payload**: `'); DROP TABLE users; --`

### 3. SQL Injection na Busca (NOVO)
**Localização**: `social/views.py` - função `search_users()`
**Tipo**: Union-based, Time-based Blind, Boolean-based Blind
**Payload**: `%' OR '1'='1`, `%' UNION SELECT ...`, `%' AND SLEEP(5) --`

### 4. SQL Injection no Perfil (NOVO)
**Localização**: `social/views.py` - função `profile()`
**Tipo**: Union-based, Time-based Blind
**Payload**: `admin' OR '1'='1 --`, `' UNION SELECT ...`

### 5. SQL Injection no Follow (NOVO)
**Localização**: `social/views.py` - funções `follow_user()` e `unfollow_user()`
**Tipo**: Stacked Queries
**Payload**: `1; UPDATE users SET password='hacked' --`

### 6. SQL Injection no Feed
**Localização**: `social/views.py` - função `feed()`
**Tipo**: Manipulação de queries
**Payload**: `1 OR 1=1`

---

## 🚀 Como Usar

### Instalação Rápida

```bash
# 1. Instalar dependências
pip install django mysqlclient python-dotenv

# 2. Criar banco de dados
sudo mysql -u root -e "CREATE DATABASE social_vulnerable CHARACTER SET utf8mb4;"

# 3. Executar migrações
python3 manage.py migrate

# 4. Iniciar servidor
python3 manage.py runserver 0.0.0.0:8000
```

### Acessar a Aplicação

| Página | URL |
|--------|-----|
| Cadastro | `http://localhost:8000/register/` |
| Login | `http://localhost:8000/login/` |
| Feed | `http://localhost:8000/feed/` |
| Buscar | `http://localhost:8000/search/` |
| Perfil | `http://localhost:8000/profile/username/` |

---

## 🧪 Exemplos de SQL Injection

### Busca: Retornar Todos os Usuários
```
URL: /search/?q=%' OR '1'='1
```

### Busca: Extrair Senhas
```
URL: /search/?q=%' UNION SELECT id, username, password, email FROM users --
```

### Perfil: Bypass
```
URL: /profile/admin' OR '1'='1 --/
```

### Perfil: Extrair Senhas
```
URL: /profile/' UNION SELECT id, username, password, email, created_at FROM users --/
```

### Login: Bypass de Autenticação
```
Username: admin' --
Password: qualquer_coisa
```

### Busca: Time-based Blind
```
URL: /search/?q=%' AND SLEEP(5) --
```

---

## 📚 Documentação Completa

- **PAYLOADS.md** - Guia original de payloads SQL Injection
- **PAYLOADS_BUSCA_FOLLOW.md** - Novos payloads para busca e follow
- **QUICK_START.md** - Guia rápido de instalação

---

## 🛡️ Como Proteger (Educação)

### ✅ Usar Prepared Statements

**Código Vulnerável**:
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Código Seguro**:
```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

### ✅ Validar Entrada

```python
import re
if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
    raise ValueError("Username inválido")
```

### ✅ Usar ORM (Object-Relational Mapping)

**Django ORM - Seguro**:
```python
user = User.objects.filter(username=username).first()
```

### ✅ Implementar Escape de Caracteres

```python
import MySQLdb
escaped_username = MySQLdb.escape_string(username)
```

### ✅ Usar Stored Procedures

```sql
CREATE PROCEDURE GetUser(IN p_username VARCHAR(100))
BEGIN
    SELECT * FROM users WHERE username = p_username;
END;
```

---

## 🎓 Casos de Uso Educacionais

1. **Aulas de Segurança Web**: Demonstrar vulnerabilidades reais
2. **Laboratórios Práticos**: Testar técnicas de SQL Injection
3. **Workshops**: Ensinar como proteger aplicações
4. **Pesquisa**: Estudar padrões de ataque e defesa
5. **Certificações**: Preparar para exames de segurança (CEH, OSCP)

---

## ⚠️ Avisos Importantes

- **Uso exclusivamente educacional**: Não use em produção
- **Ambiente de teste autorizado**: Use apenas em ambientes controlados
- **Fins de aprendizado**: Estude as vulnerabilidades e aprenda como proteger
- **Responsabilidade**: Respeite a privacidade e a segurança de outros

---

## 📞 Suporte

Para dúvidas sobre:
- **Django**: https://docs.djangoproject.com
- **SQL Injection**: https://owasp.org/www-community/attacks/SQL_Injection
- **Segurança Web**: https://portswigger.net/web-security

---

## 📝 Changelog

### v2.0 (Fevereiro 2026)
- ✅ Sistema de busca de usuários com SQL Injection
- ✅ Sistema de follow/unfollow
- ✅ Feed inteligente com priorização
- ✅ Perfil aprimorado com estatísticas
- ✅ Documentação de novos payloads
- ✅ Templates atualizados

### v1.0 (Janeiro 2026)
- ✅ Autenticação com SQL Injection
- ✅ Feed básico de postagens
- ✅ Perfil de usuário
- ✅ Interface elegante

---

**Desenvolvido para fins educacionais sobre segurança de aplicações web.**
