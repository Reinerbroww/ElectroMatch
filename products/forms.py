from django import forms
from .models import Product, Category, Criteria, ProductValue


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: ASUS ROG Strix G15'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: ASUS'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 15000000'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ['name', 'type', 'weight']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Harga, RAM, Storage'
            }),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 0.3 (total semua harus = 1.0)',
                'step': '0.01',
                'min': '0',
                'max': '1'
            }),
        }


class ProductValueForm(forms.ModelForm):
    class Meta:
        model = ProductValue
        fields = ['product', 'criteria', 'value']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'criteria': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 16 (untuk RAM 16GB)',
                'step': '0.01'
            }),
        }