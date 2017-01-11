from django import forms
from django.core.exceptions import ValidationError

from Olympiad.helpers import run_query


class NewFeolForm(forms.Form):
    name = forms.CharField(label='نام')
    t_t = forms.IntegerField(label='تعداد طلا')
    t_n = forms.IntegerField(label='تعداد نقره')
    groups = forms.CharField(label='گروه ها')


class NewOlForm(forms.Form):
    yr = forms.IntegerField(label='سال')
    saghf = forms.IntegerField(label='سقف افتادن')
    t_m1 = forms.IntegerField(label='تعداد قبولی مرحله اول')
    t_m2 = forms.IntegerField(label='تعداد قبولی مرحله دوم')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feol'] = forms.ChoiceField(
            choices=[(x['fname'], x['fname']) for x in
                     run_query("select fname from Field", fetch=True)], label='رشته'
        )


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
