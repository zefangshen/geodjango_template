from pathlib import Path
from django.core.management.base import BaseCommand, CommandParser
from visualisation.models import Vector
import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry

from ipdb import set_trace

class Command(BaseCommand):
    help = 'populate the vector data table with Brexit data'

    def add_arguments(self, parser):
        parser.add_argument(
            'action', type=str, help='create or rm records in db'
        )
        # parser.add_argument('--create', type=str, help='create records in db')

    def handle(self, *args, **options):

        action = options['action']

        if action == 'create':
            # read data
            df_file = Path.cwd() / 'data' / 'brexit.gpkg'
            gdf = gpd.read_file(df_file)

            # add to table
            for _, row in gdf.iterrows():
                if row['geometry'].geom_type == 'Polygon':
                    vector = Vector.objects.create(
                        name = row['lad16nm'],
                        code = row['lad16cd'],
                        pct_leave = row['Pct_Leave'],
                        poly = GEOSGeometry(row['geometry'].wkt),
                        multipoly = None
                    )
                elif row['geometry'].geom_type == 'MultiPolygon':
                    vector = Vector.objects.create(
                        name = row['lad16nm'],
                        code = row['lad16cd'],
                        pct_leave = row['Pct_Leave'],
                        poly = None,
                        multipoly = GEOSGeometry(row['geometry'].wkt)
                    )

                vector.save()

            print('Vector data added to database.')

        elif action == 'clear':
            Vector.objects.all().delete()
            print('All records have been removed')
