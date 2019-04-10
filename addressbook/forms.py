from django import forms
from .models import AddressBookList


class AddressBookListForm(forms.ModelForm):
    class Meta:
        model = AddressBookList
        fields = ('fname', 'lname', 'cnumber', 'address', )
