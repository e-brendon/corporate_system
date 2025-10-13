import random
import string
import secrets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
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
        self.allow_group_selection = kwargs.pop('allow_group_selection', False)
        self.group_queryset = kwargs.pop('group_queryset', Group.objects.all())
        self.generated_password = None
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if self.auto_generate_password:
            self.fields.pop('password1')
            self.fields.pop('password2')
        if self.allow_group_selection:
            self.fields['group'] = forms.ModelChoiceField(
                queryset=self.group_queryset,
                label='Grupo',
                required=True,
                empty_label='Selecione um grupo'
            )
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        if 'group' in self.fields and isinstance(self.fields['group'].widget, forms.Select):
            self.fields['group'].widget.attrs['class'] = 'form-select'

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
            self.save_m2m()
            if self.allow_group_selection:
                group = self.cleaned_data.get('group')
                if group:
                    user.groups.set([group])
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
        self.group_queryset = kwargs.pop('group_queryset', Group.objects.all())
        super().__init__(*args, **kwargs)
        can_manage_groups = self.user and self.user.groups.filter(name__in=['administrador','colaborador']).exists()
        if can_manage_groups:
            current_group = None
            if self.instance and self.instance.pk:
                current_group = self.instance.groups.first()
            self.fields['group'] = forms.ModelChoiceField(
                queryset=self.group_queryset,
                label='Grupo',
                required=True,
                initial=current_group,
                empty_label=None,
            )
        else:
            for field_name in ['is_active']:
                if field_name in self.fields:
                    del self.fields[field_name]
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        if 'group' in self.fields and isinstance(self.fields['group'].widget, forms.Select):
            self.fields['group'].widget.attrs['class'] = 'form-select'

    def save(self, commit=True):
        user = super().save(commit=commit)
        if 'group' in self.cleaned_data and commit:
            group = self.cleaned_data.get('group')
            if group:
                user.groups.set([group])
            else:
                user.groups.clear()
        return user
