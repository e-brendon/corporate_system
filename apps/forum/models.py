from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

user = get_user_model()

# Create your models here.
class PostagemForum(models.Model):
    usuario = models.ForeignKey(user, related_name="user_postagem_forum", on_delete=models.CASCADE)  
    titulo = models.CharField('Titulo',max_length=100)
    descricao = models.TextField('Descrição',max_length=350) 
    data_publicacao = models.DateField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField('Publicar Postagem?', default=False)
    anexar_imagem = models.ImageField('Imagem Anexo', upload_to='postagem-forum/', blank=True, null=True)
    
    def __str__(self):
        return "{} ({})".format(self.titulo, self.data_publicacao)

    class Meta:
        verbose_name = 'Postagem Forum'
        verbose_name_plural = 'Postagem Forum'
        ordering = ['-data_criacao']


class ComentarioPostagemForum(models.Model):
    postagem = models.ForeignKey(
        PostagemForum,
        related_name='comentarios',
        on_delete=models.CASCADE,
    )
    usuario = models.ForeignKey(user, related_name='comentarios_forum', on_delete=models.CASCADE)
    conteudo = models.TextField('Comentário', max_length=750)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='respostas',
        on_delete=models.CASCADE,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comentário de {self.usuario} em {self.postagem}"

    class Meta:
        verbose_name = 'Comentário da Postagem'
        verbose_name_plural = 'Comentários das Postagens'
        ordering = ['criado_em']
