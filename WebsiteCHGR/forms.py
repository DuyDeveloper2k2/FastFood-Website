from django import forms
from .models import Khachhang

class LoginForm(forms.Form):
    sdt = forms.CharField(max_length=15, label="Số điện thoại", widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    mk = forms.CharField(max_length=50, label="Mật khẩu", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

class RegistrationForm(forms.ModelForm):
    xacnhanmatkhau = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput)

    class Meta:
        model = Khachhang
        fields = [
            'tenkhachhang', 'gioitinh', 'ngaysinh',
            'diachi', 'sodienthoai', 'email', 'cccd', 'matkhau'
        ]
        widgets = {
            'ngaysinh': forms.DateInput(attrs={'type': 'date'}),
            'matkhau': forms.PasswordInput(),
        }

class EditForm(forms.ModelForm):
    class Meta: 
        model = Khachhang
        fields = ['email', 'sodienthoai', 'ngaysinh', 'gioitinh', 'diachi', 'cccd']
        widgets = {
            'ngaysinh': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.Form):
    cartTotal = forms.IntegerField()
    bank_code = forms.CharField(max_length=20, required=False)