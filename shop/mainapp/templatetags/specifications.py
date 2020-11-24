from django import template
from django.utils.safestring import mark_safe
from ..models import Smartphone
register = template.Library()

TABLE_HEAD = """
        <table class="table">
            <tbody>
"""

TABLE_TAIL = """
             </tbody>
        </table>
"""

TABLE_CONTENT = """
          <tr>
              <td>{name}</td>
              <td>{value}</td>
          </tr>
"""
PRODUCT_SPEC = {
    'notebook': {
        'Диагнональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процесора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видиокарта': 'video',
        'Время работи акамулятора': 'time_without_charge'
    },
    'smartphone': {
        'Диагнональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разшерение екрана': 'resolution',
        'Обьем батареи': 'accum_value',
        'Оперативная память': 'ram',
        'Наличие слота для SD кары': 'sd',
        'Максимальный обьем SD карты': 'sd_volume_max',
        'Главная камера (МП)': 'main_cam_mp',
        'Фронтальная камера (МП)': 'frontal_cam_mp',

    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    # if isinstance(product, Smartphone):
    #     if not product.sd:
    #         PRODUCT_SPEC['smartphone'].pop('Максимальный обьем SD карты')
    #     else:
    #         PRODUCT_SPEC['smartphone']['Максимальный обьем SD карты'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)