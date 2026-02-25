from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .models import User, Post, Follow
import json
from django.http import JsonResponse

def index(request):
    """Página inicial - redireciona para feed se autenticado"""
    if 'user_id' in request.session:
        return redirect('feed')
    return redirect('login')

def register(request):
    """Cadastro com SQL Injection vulnerável"""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        bio = request.POST.get('bio', '')

        # VULNERÁVEL A SQL INJECTION
        query = f"""
            INSERT INTO users (username, email, password, bio, created_at, updated_at)
            VALUES ('{username}', '{email}', '{password}', '{bio}',  CURRENT_TIMESTAMP,  CURRENT_TIMESTAMP)
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
            return redirect('login')
        except Exception as e:
            return render(request, 'social/register.html', {'error': str(e)})

    return render(request, 'social/register.html')

def login(request):
    """Login com SQL Injection vulnerável"""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # VULNERÁVEL A SQL INJECTION
        query = f"""
            SELECT id, username, email FROM users 
            WHERE username = '{username}' AND password = '{password}'
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = cursor.fetchone()
            
            if user:
                request.session['user_id'] = user[0]
                request.session['username'] = user[1]
                request.session['email'] = user[2]
                return redirect('feed')
            else:
                return render(request, 'social/login.html', {'error': 'Usuário ou senha inválidos'})
        except Exception as e:
            return render(request, 'social/login.html', {'error': str(e)})

    return render(request, 'social/login.html')

def logout(request):
    """Logout do usuário"""
    request.session.flush()
    return redirect('login')

def feed(request):
    """Feed com postagens de quem você segue em destaque"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session.get('user_id')
    
    # Buscar IDs dos usuários que o usuário segue
    following_query = f"""
        SELECT following_id FROM follows WHERE follower_id = {user_id}
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(following_query)
            following_ids = [row[0] for row in cursor.fetchall()]
        
        my_posts_query = f"""
            SELECT p.id, p.content, p.created_at, u.username, u.id as user_id, 2 as is_followed
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id = {user_id}
            ORDER BY p.created_at DESC
        """

        # Buscar postagens de quem você segue (em destaque)
        if following_ids:
            following_ids_str = ','.join(map(str, following_ids))
            followed_posts_query = f"""
                SELECT p.id, p.content, p.created_at, u.username, u.id as user_id, 1 as is_followed
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id IN ({following_ids_str})
                ORDER BY p.created_at DESC
            """
        else:
            followed_posts_query = "SELECT NULL LIMIT 0"
        
        # Buscar postagens de outros usuários (em baixo)
        other_posts_query = f"""
            SELECT p.id, p.content, p.created_at, u.username, u.id as user_id, 0 as is_followed
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id NOT IN (SELECT following_id FROM follows WHERE follower_id = {user_id})
            AND p.user_id != {user_id}
            ORDER BY p.created_at DESC
        """
        
        with connection.cursor() as cursor:
            cursor.execute(my_posts_query)
            my_posts = cursor.fetchall()
            
            cursor.execute(followed_posts_query)
            followed_posts = cursor.fetchall()
            
            cursor.execute(other_posts_query)
            other_posts = cursor.fetchall()
        
        posts = list(followed_posts) + list(other_posts) + list(my_posts)
        
        context = {
            'posts': posts,
            'username': request.session.get('username'),
            'user_id': user_id
        }
        return render(request, 'social/feed.html', context)
    except Exception as e:
        return render(request, 'social/feed.html', {'error': str(e)})

def search_users(request):
    """Busca de usuários com SQL Injection vulnerável"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session.get('user_id')
    query_term = request.GET.get('q', '')
    results = []
    
    if query_term:
        # VULNERÁVEL A SQL INJECTION - Concatenação direta
        search_query = f"""
            SELECT id, username, email, bio FROM users 
            WHERE (username LIKE '%{query_term}%' OR email LIKE '%{query_term}%')
            AND id != {user_id}
            LIMIT 20
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(search_query)
                results = cursor.fetchall()
                
                # Buscar informações de follow para cada usuário
                for i, result in enumerate(results):
                    search_user_id = result[0]
                    follow_check_query = f"""
                        SELECT COUNT(*) FROM follows 
                        WHERE follower_id = {user_id} AND following_id = {search_user_id}
                    """
                    cursor.execute(follow_check_query)
                    is_following = cursor.fetchone()[0] > 0
                    results[i] = result + (is_following,)
        except Exception as e:
            return render(request, 'social/search.html', {'error': str(e), 'query': query_term})
    
    context = {
        'results': results,
        'query': query_term,
        'username': request.session.get('username'),
        'user_id': user_id
    }
    return render(request, 'social/search.html', context)

def follow_user(request, user_id):
    """Seguir um usuário com SQL Injection vulnerável"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    follower_id = request.session.get('user_id')
    
    # VULNERÁVEL A SQL INJECTION
    follow_query = f"""
        INSERT OR IGNORE INTO follows (follower_id, following_id, created_at)
        VALUES ({follower_id}, {user_id}, CURRENT_TIMESTAMP)
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(follow_query)
    except Exception as e:
        pass
    
    # Obter o nome do usuário seguido
    get_username_query = f"SELECT username FROM users WHERE id = {user_id}"
    with connection.cursor() as cursor:
        cursor.execute(get_username_query)
        username = cursor.fetchone()[0]
    
    return redirect('profile', username=username)

def unfollow_user(request, user_id):
    """Deixar de seguir um usuário com SQL Injection vulnerável"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    follower_id = request.session.get('user_id')
    
    # VULNERÁVEL A SQL INJECTION
    unfollow_query = f"""
        DELETE FROM follows 
        WHERE follower_id = {follower_id} AND following_id = {user_id}
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(unfollow_query)
    except Exception as e:
        pass
    
    # Obter o nome do usuário seguido
    get_username_query = f"SELECT username FROM users WHERE id = {user_id}"
    with connection.cursor() as cursor:
        cursor.execute(get_username_query)
        username = cursor.fetchone()[0]
    
    return redirect('profile', username=username)

def profile(request, username):
    """Perfil do usuário com SQL Injection vulnerável"""
    # VULNERÁVEL A SQL INJECTION
    query = f"SELECT id, username, email, bio, created_at FROM users WHERE username = '{username}'"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            user_data = cursor.fetchone()
        
        if not user_data:
            return render(request, 'social/profile.html', {'error': 'Usuário não encontrado'})
        
        user_id = user_data[0]
        
        # Buscar postagens do usuário
        posts_query = f"SELECT id, content, created_at FROM posts WHERE user_id = {user_id} ORDER BY created_at DESC"
        with connection.cursor() as cursor:
            cursor.execute(posts_query)
            posts = cursor.fetchall()
        
        # Buscar informações de follow
        is_following = False
        follower_count = 0
        following_count = 0
        
        if 'user_id' in request.session:
            current_user_id = request.session.get('user_id')
            follow_check_query = f"""
                SELECT COUNT(*) FROM follows 
                WHERE follower_id = {current_user_id} AND following_id = {user_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(follow_check_query)
                is_following = cursor.fetchone()[0] > 0
                
                # Contar seguidores
                cursor.execute(f"SELECT COUNT(*) FROM follows WHERE following_id = {user_id}")
                follower_count = cursor.fetchone()[0]
                
                # Contar seguindo
                cursor.execute(f"SELECT COUNT(*) FROM follows WHERE follower_id = {user_id}")
                following_count = cursor.fetchone()[0]
        
        context = {
            'user': {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'bio': user_data[3],
                'created_at': user_data[4]
            },
            'posts': posts,
            'is_own_profile': request.session.get('username') == username if 'user_id' in request.session else False,
            'is_following': is_following,
            'follower_count': follower_count,
            'following_count': following_count
        }
        return render(request, 'social/profile.html', context)
    except Exception as e:
        return render(request, 'social/profile.html', {'error': str(e)})

def my_profile(request):
    """Perfil do usuário autenticado"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    username = request.session.get('username')
    return redirect('profile', username=username)

def create_post(request):
    """Criar postagem com SQL Injection vulnerável"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        content = request.POST.get('content', '')
        user_id = request.session.get('user_id')
        
        # VULNERÁVEL A SQL INJECTION
        query = f"""
            INSERT INTO posts (user_id, content, created_at, updated_at)
            VALUES ({user_id}, '{content}',  CURRENT_TIMESTAMP,  CURRENT_TIMESTAMP)
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
            return redirect('feed')
        except Exception as e:
            return render(request, 'social/feed.html', {'error': str(e)})
    
    return redirect('feed')


def delete_post(request, post_id):
    if 'user_id' not in request.session:
        return JsonResponse({"success": False, "message": "Não autenticado"})

    current_user_id = request.session.get('user_id')

    try:
        with connection.cursor() as cursor:

            # Buscar role do usuário
            role_query = f"""
                SELECT role FROM users WHERE id = {current_user_id}
            """
            cursor.execute(role_query)
            result = cursor.fetchone()

            if not result:
                return JsonResponse({"success": False, "message": "Usuário não encontrado"})

            role = result[0]

            # Se for admin → pode deletar qualquer post
            if role == "admin":
                delete_query = f"""
                    DELETE FROM posts WHERE id = {post_id}
                """
            else:
                # Usuário normal só pode deletar o próprio post
                delete_query = f"""
                    DELETE FROM posts 
                    WHERE id = {post_id} AND user_id = {current_user_id}
                """

            cursor.execute(delete_query)

            if cursor.rowcount == 0:
                return JsonResponse({
                    "success": False,
                    "message": "Você não tem permissão para deletar este post"
                })

        return JsonResponse({
            "success": True,
            "message": "Post deletado com sucesso"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })