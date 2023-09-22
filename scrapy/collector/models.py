from django.db import models

# Create your models here.
class Collector(models.Model) :
    platformcode = models.TextField(db_column='PlatformCode', blank=True, null=True)  # Field name made lowercase.
    country = models.TextField(db_column='Country', blank=True, null=True)  # Field name made lowercase.
    npv = models.TextField(db_column='NPV', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    shelf = models.TextField(db_column='Shelf', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return f'{self.country}_{self.npv}'