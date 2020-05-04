from django import forms
from django.forms import TextInput, Select, PasswordInput, FileInput, Textarea
from item.models import Item, ItemCategory, ItemColor, ItemImage, ItemLabel, ItemSize, ItemQuantitySize


class ItemImageForm(forms.ModelForm):
    image = forms.ImageField(widget=FileInput(
        attrs={'class': 'input_prova'}))

    class Meta:
        model = ItemImage
        fields = ('image', )


class ItemQuantitySizeForm(forms.ModelForm):
    class Meta:
        model = ItemQuantitySize
        fields = '__all__'


class ItemForm(forms.ModelForm):
    img = forms.ImageField(required=True, widget=FileInput(
        attrs={'class': 'input_prova'}))
    name = forms.CharField(max_length=100, help_text='title')
    category = forms.ModelChoiceField(queryset=ItemCategory.objects.all())
    color = forms.ModelMultipleChoiceField(queryset=ItemColor.objects.all())
    # size = forms.ModelMultipleChoiceField(queryset=ItemSize.objects.all())
    description = forms.CharField(widget=Textarea)
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    # quantity = forms.IntegerField()

    class Meta:
        model = Item
        fields = ['name', 'description',
                  'category', 'price', 'img', 'color']
