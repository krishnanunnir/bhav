from django.db import models
from django.utils import timezone
STATUS = (
    (1, 'SUCCESS'),
    (0, 'FAILURE'),
)
# Create your models here.
class ImportDetails(models.Model):
    """
    Details about the import and its status
    """
    imported_date = models.DateField(auto_now= True)
    imported_time = models.TimeField(auto_now=True)
    status = models.IntegerField(choices= STATUS, default= 0)

class ImportDate(models.Model):
    """
    Data about equity added to this db
    """
    # Storing as CharField as we won't use as number.
    code = models.CharField(max_length= 6)
    name = models.CharField(max_length= 26)
    # Storing as Integer for future usage
    open_value = models.IntegerField()
    high_value = models.IntegerField()
    low_value = models.IntegerField()
    close_value = models.IntegerField()
    imported_details = models.ForeignKey(ImportDetails, on_delete=models.CASCADE)