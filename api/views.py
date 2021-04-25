import datetime
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from .serializers import EquitySerializer
from .Pagination import PageNumberCountPagination
from rest_framework.decorators import api_view

@api_view(['GET'])
def stock_list(request):
    """
    API returning all the contents of cached data
    since there is only one method, I don't think there is need for abstracts and such like viewsets
    """
    if request.method=="GET":
        # paginating with our own paginator for future extensability
        paginator = PageNumberCountPagination()
        paginator.page_size = 200
        all_stocks = []
        # keys are not ideal in very large caches
        # but our cache at max contains 4000 records corresponding to equity csv
        # wildcards can be used with cache keys
        stock_list =  cache.keys("*")
        # using the stock list to retrieve the values from cache
        # excluding the latest value in cache which contains the last day it was updated
        for stock in [x for x in stock_list if x!="latest"]:
            all_stocks+=[cache.get(stock)]
        result_page = paginator.paginate_queryset(all_stocks, request)
        serializer = EquitySerializer(result_page,many= True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def stock_list_by_name(request):
    """
    API returning the all the stocks containing the stockname pattern
    """
    if request.method=="GET":
        stockname = request.GET.get("stockname")
        paginator = PageNumberCountPagination()
        paginator.page_size = 200
        search_result = []
        # very similar to stock_list method, in cache keys we are adding the name of stock we are searching for
        search_key = cache.keys("*"+stockname.lower() +"*")
        for key in [x for x in search_key if x!="latest"]:
            search_result+=[cache.get(key)]
        result_page = paginator.paginate_queryset(search_result, request)
        serializer = EquitySerializer(result_page,many= True)
        return paginator.get_paginated_response(serializer.data)