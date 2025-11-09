from django.db import models


class EmpresaContato(models.Model):
    nome_empresa = models.CharField('Nome da empresa', max_length=120, blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    discord_url = models.URLField('Discord', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contato da Empresa'
        verbose_name_plural = 'Contatos da Empresa'

    def __str__(self):
        return self.nome_empresa or 'Contatos da Empresa'

    @classmethod
    def obter_unico(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj


class HomePageConfig(models.Model):
    mostrar_ultimas_postagens = models.BooleanField('Mostrar últimas 5 postagens', default=False)
    mostrar_postagens_interagidas = models.BooleanField('Mostrar postagens com mais interações', default=False)
    mostrar_secao_sobre = models.BooleanField('Mostrar seção "Sobre"', default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração da Página Inicial'
        verbose_name_plural = 'Configuração da Página Inicial'

    def __str__(self):
        return 'Configuração da Página Inicial'

    @classmethod
    def obter_unico(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj
