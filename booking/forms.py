from django import forms
from models import StepOne, StepTwo, StepThree, StepFour, StepFive, StepSix, StepSeven, StepEight

class StepOneForm(forms.ModelForm):
    class Meta:
        model = StepOne
        exclude = ['session']

class StepTwoForm(forms.ModelForm):
    class Meta:
        model = StepTwo
        exclude = ['session']

class StepThreeForm(forms.ModelForm):
    class Meta:
        model = StepThree
        exclude = ['session']
        

class StepFourForm(forms.ModelForm):
    class Meta:
        model = StepFour
        exclude = ['session']
        widgets = {
            'street': forms.TextInput(),
            'city': forms.TextInput(),
        }

class StepFiveForm(forms.ModelForm):
    class Meta:
        model = StepFive
        exclude = ['session']

class StepSixForm(forms.ModelForm):
    cleaning_datetime = forms.DateTimeField(label="Time of cleaning", input_formats=["%Y-%m-%dT%H:%M:%S"])

    class Meta:
        model = StepSix
        exclude = ['session']

class StepSevenForm(forms.ModelForm):
    class Meta:
        model = StepSeven
        exclude = ['session']
        widgets = {
            'phone': forms.TextInput(),
            'fullname': forms.TextInput(),
            'referral': forms.TextInput(),
        }

class StepEightForm(forms.ModelForm):
    class Meta:
        model = StepEight
        exclude = ['session']