from django import forms

from perfil.models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'foto',
            'ocupacao',
            'descricao',
            'genero',
            'telefone',
            'cidade',
            'estado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_foto = self.instance.foto.name if self.instance and self.instance.foto else None
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{classes} form-control'.strip()
        self.fields['foto'].widget.attrs['accept'] = 'image/*'

    def save(self, commit=True):
        perfil = super().save(commit=False)
        foto_field = self.cleaned_data.get('foto')
        foto_cleared = foto_field is False

        if foto_cleared:
            perfil.foto = ''

        if commit:
            perfil.save()
            self.save_m2m()

            new_foto_name = perfil.foto.name if perfil.foto else None
            if self._original_foto and (foto_cleared or new_foto_name != self._original_foto):
                storage = perfil.foto.storage
                if storage.exists(self._original_foto):
                    storage.delete(self._original_foto)
        return perfil
