from django.template import Library

register=Library()

@register.simple_tag()
def gen_role_url(role_id,request):
    query_dict=request.GET.copy()
    query_dict['rid']=role_id
    return query_dict.urlencode()
