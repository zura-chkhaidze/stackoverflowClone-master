from django import forms
from forum.models import Answer, Question, Tag
from users.models import User


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'title', 'text'
        ]


    tags = forms.ModelMultipleChoiceField(Tag.objects.all())

    def save(self, user, commit=True,):
        question =super().save(commit=False)
        question.user = user
        question.save()
        print(self.cleaned_data['tags'])
        question.tag_set.add(*self.cleaned_data['tags'])
        return question




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
        fields = ['text']
