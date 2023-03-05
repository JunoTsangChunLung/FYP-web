from django import forms
from .models import Product, Category, Subcategory


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name', 'inventory','quantity_produced', 'min_price', 'max_price', 'period'
        ]
        labels = {
            'period':'Sales Period (Day)'
        } 

class CategoryForm(forms.Form):
    
    category = forms.ChoiceField(choices=[])
    subcategory = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = choices
        self.fields['subcategory'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        category_id = cleaned_data.get('category')
        if category_id:
            category = Category.objects.get(id=category_id)
            subcategories = [(s.id, s.name) for s in category.subcategories.all()]
            self.fields['subcategory'].choices = subcategories
        return cleaned_data
