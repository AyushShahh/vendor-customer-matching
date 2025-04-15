from django import forms
from business.models import Business, BusinessCategory
from product.models import Product, ProductCategory


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description', 'city', 'area', 'state', 'phone_number', 'address', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'cost_price', 'selling_price', 'quantity', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SaleForm(forms.Form):
    product = forms.ModelChoiceField(queryset=None)
    quantity = forms.IntegerField(min_value=1)
    
    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super(SaleForm, self).__init__(*args, **kwargs)
        
        if business:
            self.fields['product'].queryset = Product.objects.filter(business=business, quantity__gt=0)