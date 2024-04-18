from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import News

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=255)

    class Meta:
        model = News
        fields = ['title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_title(self):
        title = self.cleaned_data['title']
        news = News.objects.filter(title=title).first()

        
        if not news:
            return title

        if news.added_by.filter(id=self.user.id).exists():
            raise forms.ValidationError('Вы уже добавили эту тему')
        
        return title

    def save(self, commit=True):
        title = self.cleaned_data['title']
        try:
            news = News.objects.get(title=title)
            news.added_by.add(self.user)
            news.popularity += 1
            news.save()
        except News.DoesNotExist:
            news = super().save(commit=False)
            news.save()
            news.added_by.add(self.user)
        return news