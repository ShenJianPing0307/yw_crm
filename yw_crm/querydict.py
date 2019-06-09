# from django.http.request import QueryDict
#
#
# query_dict=QueryDict(mutable=True)
# query_dict['name']='东风汽车'
# query_dict['location']='小荷'
#
# _filter=query_dict.urlencode()
# print(_filter)

from urllib.parse import urlencode

url_dict={'name':'fg','age':34}

print(urlencode(url_dict))  #age=34&name=fg