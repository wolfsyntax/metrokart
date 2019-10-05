from django.db import models

# Create your models here.
class Region(models.Model):

    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=128)

    class Meta:
        db_table = "Region"
        verbose_name = "Region"
        verbose_name_plural="Regions"

    def __str__(self):
        return self.region_name

class Province(models.Model):

    province_id = models.AutoField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    province_name = models.CharField(max_length=128)
    #province_code = models.CharField(max_length=6)

    class Meta:
        db_table = "Province"

        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return self.province_name


class City(models.Model):

    city_id = models.AutoField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=4)

    class Meta:
        db_table = "City"

        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name


class Barangay(models.Model):

    barangay_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    barangay_name = models.CharField(max_length=128)

    class Meta:
        db_table = "Barangay"
        verbose_name = "Barangay"
        verbose_name_plural = "Barangays"

    def __str__(self):
        return self.barangay_name
