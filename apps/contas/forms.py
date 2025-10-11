import random
import string
import secrets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from contas.models import MyUser 

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': 'Email', 
            'first_name': 'Nome', 
            'last_name': 'Sobrenome', 
            'is_active': 'Usúario Ativo?'
        }

    def __init__(self, *args, **kwargs):
        self.auto_generate_password = kwargs.pop('auto_generate_password', False)
        self.generated_password = None
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if self.auto_generate_password:
            self.fields.pop('password1')
            self.fields.pop('password2')
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        if self.auto_generate_password:
            return None
        return super(CustomUserCreationForm, self).clean_password2()

    def save(self, commit=True):
        password = None
        if self.auto_generate_password:
            password = self._generate_random_password()
            self.generated_password = password
            # Garantir que os métodos do formulário tenham acesso à senha gerada.
            self.cleaned_data['password1'] = password
            self.cleaned_data['password2'] = password
        else:
            self.generated_password = None

        user = super(CustomUserCreationForm, self).save(commit=False)

        if password:
            user.set_password(password)
            self._mark_user_for_password_change(user)
        else:
            user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    def _mark_user_for_password_change(self, user):
        # Set both attribute spellings to support existing database fields or
        # downstream logic that expects either name.
        setattr(user, 'force_change_password', True)
        setattr(user, 'force_chance_password', True)

    def _generate_random_password(self, length=12):
        # Ensure the password has at least one lowercase, uppercase, and digit.
        alphabet = string.ascii_letters + string.digits
        password_chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
        ]
        password_chars.extend(secrets.choice(alphabet) for _ in range(length - len(password_chars)))
        random.shuffle(password_chars)
        return ''.join(password_chars)


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name','is_active']
        help_texts = {'username': None}
        labels = {
            'email': 'Email', 
            'first_name': 'Nome', 
            'last_name': 'Sobrenome', 
            'is_active': 'Usúario Ativo?'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # get the 'user' from kwargs dictionary
        super().__init__(*args, **kwargs)
        if not self.user.groups.filter(name__in=['administrador','colaborador']).exists():
            for group in ['is_active']: 
                del self.fields[group]
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
