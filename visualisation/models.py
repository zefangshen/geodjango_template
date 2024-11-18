# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPolygon, Polygon

# Create your models here.
class Vector(models.Model):
    # brexit data
    name = models.CharField(max_length=32, default='')
    code = models.CharField(max_length=12, default='')
    pct_leave = models.FloatField(null=True)
    # default=Polygon(),
    poly = models.PolygonField(null=True, srid=4326)  # srid, spatial reference identifier
    # default=MultiPolygon,
    multipoly = models.MultiPolygonField(null=True, srid=4326)

    def __str__(self):
        return self.name

class Raster(models.Model):
    # elevation data
    name = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=128, default='')
    raster = models.RasterField(null=True, blank=True)
