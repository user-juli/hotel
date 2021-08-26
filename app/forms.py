from django import forms

class index(forms.Form):
    checkin = forms.DateTimeField()
    checkout = forms.DateTimeField()
    Options = [
        ('1'),
        ('2'),
        ('3'),
        ('4'),
      ]
    adults = forms.ChoiceField(label='Adults', widget=forms.Select, choices=Options)
