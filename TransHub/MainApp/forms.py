
from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Bus, Category, Location, Schedule, Supplier, UserProfile,Users

class UserProfileForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'phone_number']

class AdditionalProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'city', 'date_of_birth', 'profile_picture']

class SaveCategory(forms.ModelForm):
    name = forms.CharField(max_length="250")
    description = forms.Textarea()
    status = forms.ChoiceField(choices=[('1','Active'),('2','Inactive')])

    class Meta:
        model = Category
        fields = ('name','description','status')

    def clean_name(self):
        id = self.instance.id if self.instance.id else 0
        name = self.cleaned_data['name']
        # print(int(id) > 0)
        # raise forms.ValidationError(f"{name} Category Already Exists.")
        try:
            if int(id) > 0:
                category = Category.objects.exclude(id=id).get(name = name)
            else:
                category = Category.objects.get(name = name)
        except:
            return name
            # raise forms.ValidationError(f"{name} Category Already Exists.")
        raise forms.ValidationError(f"{name} Category Already Exists.")
    
class SaveLocation(forms.ModelForm):
    location = forms.CharField(max_length="250")
    status = forms.ChoiceField(choices=[('1','Active'),('2','Inactive')])

    class Meta:
        model = Location
        fields = ('location','status')

    def clean_location(self):
        id = self.instance.id if self.instance.id else 0
        location = self.cleaned_data['location']
        # print(int(id) > 0)
        try:
            if int(id) > 0:
                loc = Location.objects.exclude(id=id).get(location = location)
            else:
                loc = Location.objects.get(location = location)
        except:
            return location
            # raise forms.ValidationError(f"{location} Category Already Exists.")
        raise forms.ValidationError(f"{location} Location Already Exists.")
    
class SaveBus(forms.ModelForm):
    bus_number = forms.CharField(max_length="250")
    category = forms.CharField(max_length="250")
    seats = forms.CharField(max_length="250")
    status = forms.ChoiceField(choices=[('1','Active'),('2','Inactive')])

    class Meta:
        model = Bus
        fields = ('bus_number','category','status','seats')

    def clean_category(self):
        id = self.cleaned_data['category']
        try:
            category = Category.objects.get(id = id)
            return category
        except:
            raise forms.ValidationError(f"Invalid Category Already Exists.")
    
    def clean_bus_number(self):
        id = self.instance.id if self.instance.id else 0
        bus_number = self.cleaned_data['bus_number']
        # print(int(id) > 0)
        try:
            if int(id) > 0:
                bus = Bus.objects.exclude(id=id).get(bus_number = bus_number)
            else:
                bus = Bus.objects.get(bus_number = bus_number)
        except:
            return bus_number
            # raise forms.ValidationError(f"{bus_number} Category Already Exists.")
        raise forms.ValidationError(f"{bus_number} bus Already Exists.")
    
class SaveSchedule(forms.ModelForm):
    code = forms.CharField(max_length="250")
    bus = forms.IntegerField()
    depart = forms.IntegerField()
    destination = forms.IntegerField()
    fare = forms.FloatField(min_value=0,max_value=999999)
    schedule = forms.CharField(max_length="250")
    status = forms.ChoiceField(choices=[('1','Active'),('2','Cancelled')])

    class Meta:
        model = Schedule
        fields = ('code','bus','depart','destination','fare','schedule','status')
    def clean_code(self):
        id = self.instance.id if self.instance.id else 0
        if id > 0:
            try:
                schedule = Schedule.objects.get(id = id)
                return schedule.code
            except:
                code= ''
        else:
            code= ''
        pref = datetime.today().strftime('%Y%m%d')
        code = str(1).zfill(4)
        while True:
            sched = Schedule.objects.filter(code=str(pref + code)).count()
            if sched > 0:
                code = str(int(code) + 1).zfill(4)
            else:
                code = str(pref + code)
                break
        return code

    def clean_bus(self):
        bus_id = self.cleaned_data['bus']

        try:
            bus = Bus.objects.get(id=bus_id)
            return bus
        except:
            raise forms.ValidationError("Bus is not recognized.")
    
    def clean_depart(self):
        location_id = self.cleaned_data['depart']

        try:
            location = Location.objects.get(id=location_id)
            return location
        except:
            raise forms.ValidationError("Depart is not recognized.")
    
    def clean_destination(self):
        location_id = self.cleaned_data['destination']

        try:
            location = Location.objects.get(id=location_id)
            return location
        except:
            raise forms.ValidationError("Destination is not recognized.")
        

# form used for supplier
class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern' : '[A-Z0-9]{15}', 'title' : 'GSTIN Format Required'})
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'email', 'gstin']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }





