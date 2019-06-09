from django.template import Library


register=Library()


@register.simple_tag()
def get_val(form):

    return getattr(form.instance,"get_product_status_display")()

