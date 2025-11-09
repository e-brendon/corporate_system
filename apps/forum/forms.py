from django import forms
from django.utils import timezone
from django.utils.html import strip_tags
from .models import PostagemForum, ComentarioPostagemForum

GRUPOS_GESTAO = ('administrador', 'colaborador')

class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo']

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
        if not self.fields['data_publicacao'].initial:
            self.fields['data_publicacao'].initial = timezone.localdate()
        self.fields['descricao'].widget.attrs['required'] = False

    def _usuario_gestor(self):
        if not self.user:
            return False
        return self.user.is_superuser or self.user.groups.filter(name__in=GRUPOS_GESTAO).exists()

    def clean_data_publicacao(self):
        from django.utils import timezone
        data = self.cleaned_data.get('data_publicacao')
        return data or timezone.localdate()

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao', '')
        if not strip_tags(descricao).strip():
            raise forms.ValidationError('Informe o conteúdo da descrição.')
        return descricao

# Class para editar postagem 
class EditPostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo']

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
        if not self.fields['data_publicacao'].initial:
            self.fields['data_publicacao'].initial = timezone.localdate()
        self.fields['descricao'].widget.attrs['required'] = False

    def _usuario_gestor(self):
        if not self.user:
            return False
        return self.user.is_superuser or self.user.groups.filter(name__in=GRUPOS_GESTAO).exists()

    def clean_data_publicacao(self):
        from django.utils import timezone
        data = self.cleaned_data.get('data_publicacao')
        return data or timezone.localdate()

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao', '')
        if not strip_tags(descricao).strip():
            raise forms.ValidationError('Informe o conteúdo da descrição.')
        return descricao


class ComentarioPostagemForumForm(forms.ModelForm):
    conteudo = forms.CharField(
        label='Comentário',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'comment-editor-input d-none',
            'placeholder': 'Compartilhe sua opinião...'
        }),
    )

    class Meta:
        model = ComentarioPostagemForum
        fields = ['conteudo']

    def clean_conteudo(self):
        conteudo = self.cleaned_data.get('conteudo', '')
        if not strip_tags(conteudo).strip():
            raise forms.ValidationError('Informe o conteúdo do comentário.')
        return conteudo
