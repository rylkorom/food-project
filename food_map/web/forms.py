from django import forms
from django.contrib.auth.models import User
from .models import History


class UserRegistrationForm(forms.ModelForm):
    """form of user's registration"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """checks if password and password repeated are equals """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    """form of loging in"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    """form of editing user fields"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AddToHistory(forms.ModelForm):
    """form of adding a place to history"""

    class Meta:
        model = History
        place_of_visiting = forms.ModelChoiceField(queryset=History.objects.all(), empty_label='Выберите',
                                                   to_field_name='place_of_visiting',
                                                   widget=forms.Select(attrs={'class': 'form-control',
                                                                              'placeholder': 'choose'}))
        fields = ['place_of_visiting', 'date_of_visiting', 'comment']
        widgets = {
            'date_of_visiting': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата посещения заведения, в формате гггг-мм-дд'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Добавьте пометки для себя (по желанию) '
            })
        }
