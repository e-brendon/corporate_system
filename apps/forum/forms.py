from django import forms
from .models import PostagemForum, ComentarioPostagemForum

GRUPOS_GESTAO = ('administrador', 'colaborador')

class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo', 'anexar_imagem']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostagemForumForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        if 'ativo' in self.fields and not self.is_bound and not self.instance.pk:
            self.fields['ativo'].initial = True
        if self.user and not self._usuario_gestor():
            self.fields['data_publicacao'].widget = forms.HiddenInput()
            self.fields['data_publicacao'].required = False

    def _usuario_gestor(self):
        if not self.user:
            return False
        return self.user.is_superuser or self.user.groups.filter(name__in=GRUPOS_GESTAO).exists()

# Class para editar postagem 
class EditPostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo', 'anexar_imagem']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditPostagemForumForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        if 'ativo' in self.fields and not self.is_bound and not self.instance.pk:
            self.fields['ativo'].initial = True
        if self.user and not self._usuario_gestor():
            self.fields['data_publicacao'].widget = forms.HiddenInput()
            self.fields['data_publicacao'].required = False

    def _usuario_gestor(self):
        if not self.user:
            return False
        return self.user.is_superuser or self.user.groups.filter(name__in=GRUPOS_GESTAO).exists()


class ComentarioPostagemForumForm(forms.ModelForm):
    conteudo = forms.CharField(
        label='Comentário',
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Compartilhe sua opinião...'}),
    )

    class Meta:
        model = ComentarioPostagemForum
        fields = ['conteudo']
