import re 
from django.core.management.base import BaseCommand
from contas.models import MyUser

class Command(BaseCommand):
    help = 'Atualiza cadastros sem username, criando basedado ao e-mail'
    help = 'Updates user records without a username, creating one based on their email'
    
    def handle(self, *args, **options):
        myuser = MyUser.objects.all()
        for user in myuser:
            get_email = user.email.split('@')[0]
            username = re.sub(r'[^a-zA-Z0-9]', '', get_email)
            user.username = username
            user.save()
            
            self.style.SUCCESS(f'Username atualizado para {user.username} no email {user.email}')
            
            
            