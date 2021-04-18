import requests
import csv
import logging
import datetime
from zipfile import ZipFile
from io import BytesIO
from io import TextIOWrapper
from .models import ImportDate, ImportDetails
from celery import Celery
from celery import shared_task
logger = logging.getLogger(__name__)
from django.core.cache import cache

def getCSVContentForDate(date_of_access):
    """
    returns the content of csv file provided the current date
    """
    # x = datetime.datetime.now()
    date_of_access_string = date_of_access.strftime("%d%m%y")
    file_name_zip = f'EQ{date_of_access_string}'
    # headers required since bseindia website rejects download requests without user agent in request
    url_to_download_bhavcopy = f"https://www.bseindia.com/download/BhavCopy/Equity/{file_name_zip}_CSV.ZIP"
    headers = {'content-type': 'application/json','User-Agent': 'My User Agent 1.0'}
    response = requests.get(url_to_download_bhavcopy, headers= headers)
    # writes are expensive, so just going to access directly using ByteIO to simulate reading the zip from file
    zipfile_data = ZipFile(BytesIO(response.content),'r')
    zipfile_data_file = zipfile_data.open(f"{file_name_zip}.CSV")
    # decided to go with csv over pandas - 1. need not add a dependancy 2. csv is more light weight 3. small dataset
    return list(csv.DictReader(TextIOWrapper(zipfile_data_file, 'utf-8')))


@shared_task
def writeCSVToDB():
    """
    Imports the data from csv to database
    Not used as of now.
    """
    today = datetime.date.today()
    import_detail, created = ImportDetails.objects.get_or_create(
        imported_date= today
    )
    if created or import_detail.status == 0:
        try:
            dict_equity = getCSVContentForDate(today)
            logger.info(f"Successfuly retrived bhavcopy for {today}")
            for row in dict_equity:
                ImportDate.objects.create(
                    code = row['SC_CODE'],
                    name = row['SC_NAME'],
                    open_value = float(row['OPEN']),
                    high_value = float(row['HIGH']),
                    low_value = float(row['LOW']),
                    close_value = float(row['CLOSE']),
                    imported_details = import_detail
                )
            import_detail.status = 1
            import_detail.save()
            logger.info(f'Successfully updated {len(dict_equity)} records in the db for {today}')
        except Exception as ex:
            logger.error(f"Issue occured while retrierving the bhavcopy for  {today} :: {str(ex)}")
@shared_task
def writeCSVToCache(today = datetime.date.today()):
    """
    Imports the data from csv to Cache
    """
    try:
        dict_equity = {
            "date": today,
            "data": getCSVContentForDate(today)
        }
        logger.info(f"Successfuly retrived bhavcopy for {today}")
        cache.set("latest", dict_equity)
        logger.info(f'Successfully updated {len(dict_equity)} records in the db for {today}')
    except Exception as ex:
        logger.error(f"Issue occured while retrierving the bhavcopy for  {today} :: {str(ex)}")