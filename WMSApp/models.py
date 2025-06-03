from django.db import models

class ProductData(models.Model):
    Product = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'ProductData'
        managed = True  # Set to True for dashboard/admin

    def __str__(self):
        return self.Product

class SourceData(models.Model):
    Source = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'SourceData'
        managed = True

    def __str__(self):
        return self.Source

class ProductionDescription(models.Model):
    ProdMinDes = models.CharField(max_length=255, primary_key=True)
    SecID = models.IntegerField()

    class Meta:
        db_table = 'Production_Description'
        managed = True

    def __str__(self):
        return self.ProdMinDes

class VAPProductionData(models.Model):
    PLANT_CHOICES = [
        ('PULILAN', 'Pulilan'),
        ('TARLAC', 'Tarlac'),
    ]
    
    SHIFT_CHOICES = [
        ('DAY SHIFT', 'Day Shift'),
        ('NIGHT SHIFT', 'Night Shift'),
    ]
    
    ID = models.AutoField(primary_key=True)
    Date = models.DateField(db_column='Date')
    PlantLoc = models.CharField(max_length=255, choices=PLANT_CHOICES, null=True, db_column='PlantLoc')
    Shift = models.CharField(max_length=255, choices=SHIFT_CHOICES, null=True, db_column='Shift')
    Product = models.ForeignKey(ProductData, on_delete=models.SET_NULL, null=True, db_column='Product', to_field='Product', related_name='vap_productions')
    TimeStart = models.TimeField(db_column='TimeStart')
    TimeEnd = models.TimeField(db_column='TimeEnd')
    Total = models.CharField(max_length=100, db_column='Total')
    ProdMinDescrip = models.ForeignKey(ProductionDescription, on_delete=models.SET_NULL, null=True, db_column='ProdMinDescrip', to_field='ProdMinDes', related_name='vap_productions')
    BoilerTemp = models.IntegerField(db_column='BoilerTemp')
    CookingOilTemp = models.DecimalField(max_digits=5, decimal_places=2, db_column='CookingOilTemp')
    MetersPerMin = models.IntegerField(null=True, db_column='MetersPerMin')
    OutputTemp = models.DecimalField(max_digits=5, decimal_places=2, db_column='OutputTemp')
    InputTemp = models.DecimalField(max_digits=5, decimal_places=2, db_column='InputTemp')
    Source = models.ForeignKey(SourceData, on_delete=models.SET_NULL, null=True, db_column='Source', to_field='Source', related_name='vap_productions')
    FormaticStrokeMin = models.IntegerField(db_column='FormaticStrokeMin')
    Section = models.CharField(max_length=255, null=True, db_column='Section')
    MonthYear = models.CharField(max_length=255, null=True, db_column='MonthYear')
    
    class Meta:
        db_table = 'VAPProductionData'
        ordering = ['-Date', '-TimeStart']
        managed = True
    
    def __str__(self):
        return f"{self.Date} - {self.Shift} - {self.Product}"
    
    def save(self, *args, **kwargs):
        if self.TimeStart and self.TimeEnd:
            self.Total = self.calculate_total_time()
        super().save(*args, **kwargs)
    
    def calculate_total_time(self):
        start_total_minutes = self.TimeStart.hour * 60 + self.TimeStart.minute
        end_total_minutes = self.TimeEnd.hour * 60 + self.TimeEnd.minute
        total_minutes = end_total_minutes - start_total_minutes
        if total_minutes < 0:
            total_minutes += 24 * 60
        display_hr = total_minutes // 60
        display_min = total_minutes % 60
        return f"{int(display_hr)} hr {int(display_min):02} min"
