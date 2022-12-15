from django import forms
from .models import Account
# from multifieldclean.forms import MultiFieldCleanFormMixin

FRUIT_CHOICES= [
    ('Afghanistan', 'Afghanistan'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Malaysia', 'Malaysia'),
    ]

class RegistrationForm(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    phone_number=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter Phone Number'
    }))
    country=forms.CharField(widget=forms.Select(choices=FRUIT_CHOICES))
    email=forms.EmailField(help_text="We'll never share your email with anyone else")
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']    #no put username due we want to generate the username via email
    
    def __init__(self,*args,**kwargs):  #understand this? this is loop thru all the field of the model
        super().__init__(*args,**kwargs)
        #set placeholder for each field, some field not exist in the models.py
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        # self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        self.fields['password'].widget.attrs['placeholder']='Enter Password'
        self.fields['confirm_password'].widget.attrs['placeholder']='Repeat Password'
        for abc in self.fields:
            self.fields[abc].widget.attrs['class']='form-control'

    #check the password and confirm password matching or not,made it more user friendly
    def clean(self):      #this clean are extremely important, you can't change it to other name, to made any verification error, compare two password same or not, need use clean
        #we kept use super because super can change the way class being saved, even we didn't mention super class, the django side will automatically execute the super function inner side
        cleaned_data=super().clean()  #super also can known as modifying something
        password=cleaned_data.get('password')  
        confirm_password=cleaned_data.get('confirm_password')
        # phone_number=cleaned_data.get('phone_number')
        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password does not match")
        # elif phone_number.isdigit()== False:
        #     raise forms.ValidationError("Phone number must be number")
        return cleaned_data
    
    def clean_phone_number(self):
        phone_passed=self.cleaned_data.get("phone_number")
        if phone_passed.isdigit()==False:
            raise forms.ValidationError("Phone number must be numeric")
        return phone_passed

    #     cleanned_data=super().clean()
    #     phone_number=cleanned_data.get('phone_number')
    #     print(phone_number)