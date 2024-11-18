import json
import io
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Vector, Raster
from django.core.serializers import serialize
from ipdb import set_trace as st
import rasterio as rio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
from PIL import Image


def redirect_to_vector(request):
    return redirect('show_raster')

def show_vector_data(request):
    """Return all vectors as GeoJSON"""
    features = []

    for geom in Vector.objects.all():
        features.append({
            "type": "Feature",
            "geometry": json.loads(geom.poly.geojson) if geom.poly else \
                json.loads(geom.multipoly.geojson),
            "properties": {
                "name": geom.name,
                "code": geom.code,
                "pct_leave": geom.pct_leave
            }
        })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    context = {'geojson_data': json.dumps(geojson_data)}

    # st()

    return render(request, 'visualisation/show_vector.html', context)

def show_raster_data(request, raster_id=None):
    """Return all rasters as GeoJSON"""
    raster = Raster.objects.first()
    gdal_raster = raster.raster
    tile_url = f'/get_raster_tile/'

    context = {
        'name': raster.name,
        'bounds': list(gdal_raster.extent),
        'center': [
            float(np.mean([gdal_raster.extent[1], gdal_raster.extent[3]])),
            float(np.mean([gdal_raster.extent[0], gdal_raster.extent[2]])),
        ],
        'tile_url': tile_url,
    }

    return render(request, 'visualisation/show_raster.html', context)

def get_raster_tile(request, raster_id=None, z=None, x=None, y=None):
    raster = Raster.objects.first()
    gdal_raster = raster.raster

    # Get the band data
    band = gdal_raster.bands[0]
    data = band.data()

    # mask the nodata values
    masked_data = np.ma.masked_equal(data, band.nodata_value)

    # Normalize data to 0-255 range
    data_min = np.min(masked_data)
    data_max = np.max(masked_data)
    normalized_data = ((masked_data - data_min) * 255 / (data_max - data_min)).astype(np.uint8)

    # Create image
    img = Image.fromarray(normalized_data)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
        
    return HttpResponse(buf.getvalue(), content_type='image/png')
