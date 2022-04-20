import json
from pathlib import Path

from django.core.management.base import BaseCommand
from accounts.models import City, District, Ward

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("Populating data... Please wait!")

        with open(BASE_DIR / 'static' / 'data' / 'local.json') as f:
            data = list(json.load(f))
        for dt in range(len(data)):
            city = City.objects.create(name=data[dt]['name'], code=data[dt]['code'])

            for dtrict in data[dt]['districts']:
                district = District.objects.create(city=city, name=dtrict['name'])
                city.districts.add(district)

                for ward in dtrict['wards']:
                    w = Ward.objects.create(name=ward['name'], district=district)
                    district.wards.add(w)
        print("Everything Done!")
