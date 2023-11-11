from django.shortcuts import HttpResponse,render

class Underconstraction:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        print(f'---------------------call from middlewre before view')
        response=render(request,'app/snippet/siteunderconstraction.html')
        print(f'---------------------call from middlewre after view')
        return response