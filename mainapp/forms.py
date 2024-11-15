from django import forms
from mainapp.models import Todo
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control text-success',
                'placeholder': 'title',
                

            }), }
    
    def clean_title(self):
        title = self.cleaned_data['title']

        if title.lower() == 'title':
            raise ValidationError('Enter your task title')

        return title
        
class UpdateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description','is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control textarea'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }