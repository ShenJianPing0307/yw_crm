from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from bs4 import BeautifulSoup

class XssMiddleware(MiddlewareMixin):

    def process_response(self,request,response):
        response=XSSFilter().process(str(response.content,encoding='utf-8'))
        return HttpResponse(response)

class XSSFilter(object):

    def __init__(self):
        self.not_valid_name=[
            'script'
        ]
        self.valid_name = [
            'body'
        ]
        self.exclude_name=[
            'alert'
        ]

    def process(self,content):
        soup=BeautifulSoup(content,"html.parser")
        for tag in soup.find_all():
            if tag.name in self.not_valid_name:
                for exclude_name in self.exclude_name:
                    if exclude_name in tag.get_text():
                        tag.decompose()
        return soup.decode()
