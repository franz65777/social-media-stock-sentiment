#!/usr/bin/env python3

import requests
import ujson as json
import re
import time

PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"


def fetchObjects(**kwargs):
    # Default params values
    params = {"sort_type": "created_utc", "sort": "asc", "size": 1000}
    for key, value in kwargs.items():
        params[key] = value
    print(params)
    type = "comment"
    if 'type' in kwargs and kwargs['type'].lower() == "submission":
        type = "submission"
    r = requests.get(PUSHSHIFT_REDDIT_URL + "/" + type + "/search/", params=params)
    if r.status_code == 200:
        response = json.loads(r.text)
        data = response['data']
        sorted_data_by__id = sorted(data, key=lambda x: int(x['id'], 36))
        return sorted_data_by__id


def process(**kwargs):
    max_created_utc = 1446686449
    max_id = 0
    file = open("data.json", "w")
    while 1:
        nothing_processed = True
        objects = fetchObjects(**kwargs, after=max_created_utc)

        if objects is not None:
            for obj in objects:
                id = int(obj['id'], 36)
                if id > max_id:
                    nothing_processed = False
                    created_utc = obj['created_utc']
                    max_id = id
                    if created_utc > max_created_utc: max_created_utc = created_utc
                    print(json.dumps(obj, sort_keys=True, ensure_ascii=True), file=file)

            if nothing_processed: return
            max_created_utc -= 1



process(subreddit="wallstreetbets", type="comment")
