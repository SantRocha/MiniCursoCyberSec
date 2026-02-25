from django.db import models

class User(models.Model):
    """
    Modelo de usuário para a rede social.
    Vulnerável a SQL Injection nas views de login e cadastro.
    """
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class Post(models.Model):
    """
    Modelo de postagem para a rede social.
    Cada postagem pertence a um usuário.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']


class Follow(models.Model):
    """
    Modelo de seguimento entre usuários.
    Permite que um usuário siga outro usuário.
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower', 'following']),
        ]

    def __str__(self):
        return f"{self.follower.username} segue {self.following.username}"
