from django import forms
from forum.models import Answer, Question,Tag
from users.models import User




class QuestionCreateForm(forms.ModelForm):
     tags= forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

     class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        # fields = [
        #     'user'
        # ]


class SearchForm(forms.Form):
    q = forms.CharField(max_length=120,
                        widget=forms.TextInput(attrs={
                            'type': 'search',
                            'class': 'form-control me-2',
                            'placeholder': "Search",
                            'aria-label': "Search"
                        }))




class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
