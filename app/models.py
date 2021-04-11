from django.db import models

STATUS = (
    (0, 'SUCCESS'),
    (1, 'FAILURE'),
)
# Create your models here.
class ImportDetails(models.Model):
    """
    Details about the import and its status
    """
    imported_on = models.DateTimeField(auto_now= True)
    status = models.IntegerField(choices= STATUS, default= 0)
class ImportDate(models.Model):
    """
    Data about equity added to this db
    """
    # Storing as CharField as we won't use as number.
    CODE = models.CharField(max_length= 6)
    NAME = models.CharField(max_length= 26)
    # Storing as Integer for future usage
    OPEN = models.IntegerField()
    HIGH = models.IntegerField()
    LOW = models.IntegerField()
    CLOSE = models.IntegerField()