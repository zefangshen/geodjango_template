from pathlib import Path
from django.core.management.base import BaseCommand, CommandParser
from visualisation.models import Raster
import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import GDALRaster

class Command(BaseCommand):
    help = 'Import clipped raster data into the database'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'action',
            type=str,
            help='Add or remove raster data'
        )

    def handle(self, *args, **options):

        action = options['action']

        data_dir = Path.cwd() / 'data'
        
        # Expected file names
        pre_flood_path = data_dir / 'pre_DSM_clipped.tif'
        post_flood_path = data_dir / 'post_DSM_clipped.tif'

        # Check if files exist
        if not pre_flood_path.exists() or not post_flood_path.exists():
            self.stderr.write(
                self.style.ERROR(
                    'Raster files not found in specified directory'
                )
            )
            return

        if action == 'create':
            try:
                # Create pre-flood raster entry
                pre_raster = Raster.objects.create(
                    name='Pre-flood DTM',
                    description='Digital Terrain Model before flood event',
                    raster=GDALRaster(str(pre_flood_path), write=True),
                )

                # Create post-flood raster entry
                post_raster = Raster.objects.create(
                    name='Post-flood DTM',
                    description='Digital Terrain Model after flood event',
                    raster=GDALRaster(str(post_flood_path), write=True),
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully imported raster data:\n'
                        f'Pre-flood ID: {pre_raster.id}\n'
                        f'Post-flood ID: {post_raster.id}'
                    )
                )

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f'Error importing raster data: {str(e)}')
                )

        elif action == 'clear':
            Raster.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All raster data removed from the database'))

