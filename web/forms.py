from django import forms

SHOT_CHOICES = [
    ('closeup', '클로즈업 샷'),
    ('full', '풀바디 샷'),
    ('lowangle', '로우 앵글 샷'),
    ('profile', '프로필 샷'),
    ('highangle', '하이 앵글 샷'),
]

class ImageGenerationForm(forms.Form):
    api_key = forms.CharField(
        label="Gemini API Key",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'AIza...', 'class': 'form-control'})
    )
    
    reference_image = forms.FileField(
        label="참조 이미지",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    output_dir = forms.CharField(
        label="출력 폴더명",
        max_length=100,
        initial="output",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    shots = forms.MultipleChoiceField(
        label="생성할 샷",
        choices=SHOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
