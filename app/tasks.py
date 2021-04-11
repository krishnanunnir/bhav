import requests
import csv
import logging
import datetime
from zipfile import ZipFile
from io import BytesIO
from io import TextIOWrapper
from app.models import ImportDate, ImportDetails
from celery import Celery
from celery.schedules import crontab
logger = logging.getLogger(__name__)

def getCSVContentForDate(date_of_access):
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

def writeCSVToDB():
    today = datetime.date.today()
    # Checking if the process has been completed successfully for a date
    import_detail, created = ImportDetails.objects.get_or_create(
        imported_date= today
    )
    print(created)
    print(import_detail.status)
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
                    imported_date = today
                )
            import_detail.status = 1
            import_detail.save()
            logger.info(f'Successfully updated {len(dict_equity)} records in the db for {today}')
        except Exception as ex:
            status = 0
            logger.error(f"Issue occured while retrierving the bhavcopy for  {today} :: {str(ex)}")

writeCSVToDB()