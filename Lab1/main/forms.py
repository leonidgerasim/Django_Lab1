from .models import Products, Customers, OrderDetail
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class AddProductsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите название товара'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите описание товара'}))
    price = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите описание товара'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите описание товара'}))

    class Meta:
        model = Products
        fields = ('name', 'description', 'price', 'quantity')


class SearchCustomersForm(forms.Form):
    name = forms.CharField(label="Имя и фамилия", widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя и фамилию клиента',
        }))


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


class AddOrderDetailsFormProduct(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        disabled = kwargs.pop('disabled', None)
        initial = kwargs.pop('initial', None)
        super(AddOrderDetailsFormProduct, self).__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(queryset=Products.objects.all(),
                                                        disabled=disabled, label='Товар:',
                                                        initial=initial,
                                                        widget=forms.Select(attrs={
                                                            'class': 'form-control py-4',
                                                        }))

    class Meta:
        model = OrderDetail
        fields = ("product",)


class AddOrderDetailsFormQuantity(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        max_quantity = kwargs.pop('max_quantity', None)
        super(AddOrderDetailsFormQuantity, self).__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(label='Количество:',
                                                     initial=1,
                                                     validators=[MinValueValidator(1, message="Минимум 1 товар"),
                                                                 MaxValueValidator(max_quantity, message="Максимум "+str(max_quantity)+" товаров")],
                                                     widget=forms.NumberInput(attrs={
                                                         'class': 'form-control py-4',
                                                         'placeholder': 'Введите количество'
                                                     }))

    class Meta:
        model = OrderDetail
        fields = ("quantity",)




