from django import forms
from django.core.exceptions import ValidationError

from Olympiad.helpers import run_query


class RegisterForm(forms.Form):
    national_code = forms.CharField(label='کد ملی', help_text='کد ملی، نام کاربری شما خواهد بود')
    name = forms.CharField(label='نام و نام خانوادگی')
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='تکرار رمز عبور')

    def clean(self):
        data = super().clean()
        if 'password' in data and 'confirm_password' in data['password'] != data['confirm_password']:
            raise ValidationError({'password': 'رمز عبور با تکرار آن مطابقت ندارد'})
        if 'national_code' in data and \
                        run_query('select count(*) from human where national_code=%s',
                                  [data['national_code']], fetch=True)[0]['count'] > 0:
            raise ValidationError({'national_code': 'کاربر با چنین کد ملی قبلا در سایت ثبت نام شده است'})
        return data


class LoginForm(forms.Form):
    national_code = forms.CharField(label='کد ملی')
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور')

    def clean(self):
        data = super().clean()
        user = run_query('select national_code, name from human where national_code=%s and password=%s',
                  [data.get('national_code'), data.get('password')], fetch=True, raise_not_found=False)
        if len(user) == 0:
            raise ValidationError('نام کاربری یا رمز عبور نادرست است')
        data['user'] = user[0]
        return data
