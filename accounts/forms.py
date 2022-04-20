from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms

from .models import Address, City, District, Ward

User = get_user_model()


class CreateUserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Mật khẩu không khớp.",
    }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = "<ul><li>{0}</li><li>{1}</li><li>{2}</li><li>{3}</li></ul>".format(
            "Mật khẩu không được bao gồm các thông tin cá nhân bên trên.",
            "Mật khẩu phải có ít nhất 8 ký tự.",
            "Mật khẩu không được là các mật khẩu thường dùng(Ví dụ:12345678).",
            "Mật khẩu phải bao gồm cả ký tự và số.",
        )
        self.fields['username'].label = "Tên đăng nhập"

        self.fields['first_name'].label = 'Họ'
        self.fields['last_name'].label = 'Tên'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].label = 'Nhập lại mật khẩu'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Họ'
        self.fields['last_name'].label = 'Tên'


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Mật khẩu cũ"
        self.fields["new_password1"].label = "Mật khẩu mới"
        self.fields["new_password2"].label = "Nhập lại mật khẩu"

        self.fields['new_password1'].help_text = "<ul><li>{0}</li><li>{1}</li><li>{2}</li><li>{3}</li></ul>".format(
            "Mật khẩu không được bao gồm các thông tin cá nhân bên trên.",
            "Mật khẩu phải có ít nhất 8 ký tự.",
            "Mật khẩu không được là các mật khẩu thường dùng(Ví dụ:12345678).",
            "Mật khẩu phải bao gồm cả ký tự và số.",
        )


class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_name', 'home', 'city', 'district', 'ward', 'phone')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Họ tên',
            }),
            'home': forms.TextInput(attrs={
                'placeholder': 'Địa chỉ cụ thể',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Số điện thoại',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['city'].label = 'Thành phố/Tỉnh'
        self.fields['district'].label = 'Quận/Huyện'
        self.fields['ward'].label = 'Phường/Xã'
        self.fields['home'].label = 'Địa chỉ'
        self.fields['phone'].label = 'Số điện thoại'

        self.fields['city'].queryset = City.objects.all().order_by('name')
        self.fields['district'].queryset = District.objects.none()
        self.fields['ward'].queryset = Ward.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['district'].queryset = District.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.city.districts.order_by('name')

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['ward'].queryset = Ward.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.district.wards.order_by('name')


PAYMENT_CHOICES = (
    ('CK', 'Chuyển khoản'),
    ('COD', 'COD')
)


class CheckOutForm(forms.Form):
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

    # note = forms.TextInput()
    # create_new_address = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':''}),initial=True) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'payment_option'].help_text = "Trường hợp thanh toán bằng hình thức chuyển khoản vui lòng chuyển vào số tài khoản 4242 4242 4242 theo cú pháp MãĐơnHàng_Sđt"
    #     self.fields['city'].queryset = City.objects.all().order_by('name')
    #     self.fields['district'].queryset = District.objects.none()
    #     self.fields['ward'].queryset = Ward.objects.none()

    #     if 'city' in self.data:
    #         try:
    #             city_id = int(self.data.get('city'))
    #             self.fields['district'].queryset = District.objects.filter(city_id=city_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['district'].queryset = self.instance.city.districts.order_by('name')

    #     if 'district' in self.data:
    #         try:
    #             district_id = int(self.data.get('district'))
    #             self.fields['ward'].queryset = Ward.objects.filter(district_id=district_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass 
    #     elif self.instance.pk:
    #         self.fields['ward'].queryset = self.instance.district.wards.order_by('name')
