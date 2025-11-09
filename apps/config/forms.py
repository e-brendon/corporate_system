from django import forms

from config.models import EmpresaContato


class EmpresaContatoForm(forms.ModelForm):
    class Meta:
        model = EmpresaContato
        fields = ['nome_empresa', 'instagram_url', 'telegram_url', 'discord_url', 'facebook_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = False
        self.fields['instagram_url'].widget.attrs['placeholder'] = 'https://instagram.com/suaempresa'
        self.fields['telegram_url'].widget.attrs['placeholder'] = 'https://t.me/suaempresa'
