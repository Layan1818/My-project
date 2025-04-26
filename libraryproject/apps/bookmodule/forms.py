from django import forms
from .models import Book, Student, Address, Student2, Address2, ProductImage

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'edition']
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price
        
    def clean_edition(self):
        edition = self.cleaned_data['edition']
        if edition < 1:
            raise forms.ValidationError("Edition must be 1 or greater")
        return edition

class StudentForm(forms.ModelForm):
    city = forms.CharField(max_length=100)
    
    class Meta:
        model = Student
        fields = ['name', 'age']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'address') and self.instance.address:
            self.fields['city'].initial = self.instance.address.city
            
    def save(self, commit=True):
        student = super().save(commit=False)
        address, _ = Address.objects.get_or_create(city=self.cleaned_data['city'])
        student.address = address
        if commit:
            student.save()
        return student

class Student2Form(forms.ModelForm):
    cities = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter cities separated by commas'
    )
    
    class Meta:
        model = Student2
        fields = ['name', 'age']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['cities'].initial = ', '.join(
                self.instance.addresses.values_list('city', flat=True)
            )
            
    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            student.save()
            # Clear existing addresses
            student.addresses.clear()
            # Add new addresses
            cities = [city.strip() for city in self.cleaned_data['cities'].split(',')]
            for city in cities:
                if city:  # Skip empty strings
                    address, _ = Address2.objects.get_or_create(city=city)
                    student.addresses.add(address)
        return student

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['name', 'description', 'price', 'image']
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price