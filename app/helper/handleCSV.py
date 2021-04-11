import datetime
import requests
import csv
from zipfile import ZipFile
import zipfile
from io import BytesIO
from io import TextIOWrapper

def getCSVContentForDate(dateOfAccess):
    # x = datetime.datetime.now()
    dateOfAccessString = dateOfAccess.strftime("%d%m%y")
    fileNameZip = f'EQ{dateOfAccessString}'
    urlToDownloadBhavCopy = f"https://www.bseindia.com/download/BhavCopy/Equity/{fileNameZip}_CSV.ZIP"
    print(urlToDownloadBhavCopy)
    # headers required since bseindia website rejects download requests without user agent in request
    headers = {'content-type': 'application/json','User-Agent': 'My User Agent 1.0'}
    response = requests.get(urlToDownloadBhavCopy, headers= headers)
    # writes are expensive, so just going to access directly
    zipfileData = ZipFile(BytesIO(response.content),'r')
    fileVal = zipfileData.open(f"{fileNameZip}.CSV")
    return list(csv.reader(TextIOWrapper(fileVal, 'utf-8')))

dateOfAccess = datetime.datetime(2020, 4, 17)
print(getCSVContentForDate(dateOfAccess))