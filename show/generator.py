import random
from datetime import datetime, timedelta

from django.conf import settings

from generate import IMAGES, VIDEOS
from generate.json_loader import load_json

SHOW_COUNT = 20

def generate():
    objects = []

    # gen radio show objects and calendar entries
    for i in range(1, SHOW_COUNT + 1):
        # create show
        objects.append({
            "model": "show.RadioShow",
            "fields": {
                "title": "Radio Show %s Title" % i,
                "description": "Radio Show %s Description" % i,
                "content": "Radio Show %s Content" % i,
                "state": "published",
                "image": random.sample(IMAGES, 1)[0],
                "sites": {
                    "model": "sites.Site",
                    "fields": { 
                        "name": "example.com"
                    }
                },
            },
        })

    # create some entries for shows
    for i in range(0, 24, 4):
        start_hour = i
        end_hour = 23 if i + 4 == 24 else i + 4
        objects.append({
            "model": "cal.Entry",
            "fields": {
                "start": str(datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)),
                "end": str(datetime.now().replace(hour=end_hour, minute=0, second=0, microsecond=0)),
                "content": {
                    "model": "show.RadioShow",
                    "fields": {
                        "title": "Radio Show %s Title" % random.randint(1, SHOW_COUNT),
                    }
                },
                "repeat": "daily",
                "repeat_until": str((datetime.now() + timedelta(days=30)).date()),
                "calendars": {
                    "model": "cal.Calendar",
                    "fields": {
                        "title": "Calendar 1 Title",
                        "sites": {
                            "model": "sites.Site",
                            "fields": { 
                                "name": "example.com"
                            },
                        },
                    },
                },
            },
        })
    
    load_json(objects)
