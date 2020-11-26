from django.contrib import admin
from django import forms
from django.forms import  ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe
# Register your models here.
from .models import *
from PIL import Image


class SmartPhoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True,
                'style': 'background: lightgray;'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red;font-size:14px;">При загрузке изоброжения с разрешением больше {}x{} оно будет обрезано!</span>'
            .format(*Product.MAX_RESOLUTION)
        )

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_width, min_height = Product.MIN_RESOLUTION
    #     max_width, max_height = Product.MAX_RESOLUTION
    #     if image.size > Product.MAX_SIZE:
    #         raise ValidationError("Размер файла больше 3МБ!")
    #     if img.width < min_width or img.height < min_height:
    #         raise ValidationError("Разшерение изображение меньше минимального!")
    #     if img.width > max_width or img.height > max_height:
    #         raise ValidationError("Разшерение изображение больше максимального!")
    #     return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey()


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'shop/admin.html'

    form = SmartPhoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey()


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Order)
