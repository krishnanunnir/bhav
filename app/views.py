"""
DB equivalent of redis
"""
from django.shortcuts import render
import datetime
import csv
from django.core.cache import cache
# Create your views here.

def get_as_csv(request, stockname=""):
    # Create the HttpResponse object with the appropriate CSV header.
    search_result = []
    search_key = cache.keys("*"+stockname.lower()+"*")
    date_of_access_string = datetime.date.today().strftime("%d%m%y")
    if stockname:
        file_name_csv = f'EQ{date_of_access_string}_{stockname}'
    else:
        file_name_csv = f'EQ{date_of_access_string}'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name_csv}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Code', 'Name', 'Open','Close','Low', 'High'])
    for  key in search_key:
        obj = cache.get(key)
        writer.writerow([obj["code"],obj["name"],obj["open_value"],obj["close_value"],obj["low_value"],obj["high_value"]])
    return response

def render_stock(request, template = "index.html"):
    return render(request, template)
