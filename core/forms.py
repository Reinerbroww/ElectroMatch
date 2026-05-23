from django import forms
from products.models import Category

class RecommendationForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Kategori Elektronik",
        empty_label="-- Pilih Kategori --"
    )
    budget = forms.IntegerField(
        label="Budget (Rp)",
        min_value=0
    )
    kebutuhan = forms.ChoiceField(
        choices=[
            ('', '-- Pilih Kebutuhan --'),
            ('gaming', 'Gaming'),
            ('coding', 'Coding / Programming'),
            ('editing', 'Video Editing'),
            ('kuliah', 'Kuliah / Office'),
        ],
        label="Kebutuhan Utama"
    )