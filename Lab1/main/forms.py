from .models import Products, Customers
from django import forms


class AddProductsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Название Товара'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Описание Товара'}))
    price = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Описание Товара'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Описание Товара'}))

    class Meta:
        model = Products
        fields = ('name', 'description', 'price', 'quantity')


class SearchCustomersForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))


class AddCustomersForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))

    total_amount = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'
    }))
    current_account = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))
    loan = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))
    debt = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))
    loan_balance = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))
    comment = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите Имя Клиента'}))

    class Meta:
        model = Customers
        fields = ("name",
                  "total_amount",
                  "current_account",
                  "loan",
                  "debt",
                  "loan_balance",
                  "comment")





