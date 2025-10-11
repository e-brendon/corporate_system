from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):   
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil') 
    foto = models.ImageField(upload_to='perfil/foto/', blank=True)  
    ocupacao = models.CharField(max_length=120, blank=True)
    descricao = models.TextField(blank=True)  
    genero = models.CharField(max_length=20, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, blank=True) 

    def __str__(self):
        return f' Perfil: {self.usuario.email}'

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil"

    @property
    def foto_url(self):
        if self.foto:
            try:
                return self.foto.url
            except ValueError:
                pass
        default_candidates = [
            'perfil/padrao/perfil.jpg',
            'perfil/foto/padrao/perfil.jpg',
        ]
        for relative_path in default_candidates:
            if default_storage.exists(relative_path):
                return f'{settings.MEDIA_URL}{relative_path}'
        # Fallback to the first candidate even if it doesn't exist to avoid breaking image tags.
        return f'{settings.MEDIA_URL}{default_candidates[0]}'

#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_perfil(sender, **kwargs):
#    if kwargs.get('created', False):
#        Perfil.objects.create(usuario=kwargs['instance'])
