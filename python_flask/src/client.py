import json, time, requests, sys
import threading
import traceback
import logging
import Queue

from flask import Flask, Response
from datetime import timedelta

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)-7s - %(message)s',
    level=logging.INFO
)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger("telitscraper")

entwine_server_auth = ("rahul", "rahul123")

iccid_q = Queue.Queue()
outq = Queue.Queue()

content_buffers = {
    "active": [],
    "upcoming": []
}


def go(func, *args, **kwargs):
    thr = threading.Thread(target=func, args=args, kwargs=kwargs)
    thr.daemon = True
    thr.start()
    return thr

@go
def printer():
    while True:
        dic = outq.get()
        content_buffers["upcoming"].append(dic)
        print dic

def threadrunner():
    while True:
        try:
            iccid = iccid_q.get()

            url = "https://restapi3.jasper.com/rws/api/v1/devices/"+iccid

            response = requests.get(url, auth=telit_auth)
            response_json = response.json()

            data_limit = response_json["accountCustom1"]

            count = 0
            data_limit_mb = ""
            if data_limit:
                for character in data_limit:
                    if count == 2:
                        if character != ";":
                            data_limit_mb += character
                    if character == ";":
                        count += 1

                if data_limit_mb:
                    data_limit_mb = float(data_limit_mb)
                else:
                    data_limit_mb = 50 # by default

            else:
                data_limit_mb = 50 # by default

            url = "https://restapi3.jasper.com/rws/api/v1/devices/"+iccid+"/ctdUsages"

            response = requests.get(url, auth=telit_auth)
            response_json = response.json()

            data_usage = response_json["ctdDataUsage"]
            data_usage_mb = data_usage/1024./1024.

            #data_usage{simcard = "129381273"} 50
            limit_out = 'data_limit_mb{iccid="'+iccid+'"} '+str(data_limit_mb)
            usage_out = 'data_usage_mb{iccid="'+iccid+'"} '+str(data_usage_mb)

            outq.put(limit_out + "\n" + usage_out)
            time.sleep(1)
        except:
            logger.debug("probably rate-limited")
            iccid_q.put(iccid)

for _ in range(7):
    go(threadrunner)


app  = Flask(__name__)

@app.route("/")
def hai():
    return Response("""<a href="/metrics">metrics</a>""")

@app.route("/metrics")
def metrics():
    return Response('\n'.join(content_buffers["active"] + ['']), mimetype="text/plain")

@app.route("/peek")
def peek():
    return Response('\n'.join(content_buffers["upcoming"] + ['']), mimetype="text/plain")

@app.route("/metrics.json")
def metrics_json():
    return Response(json.dumps(content_buffers["active"]), mimetype="application/json")

def main():
    app.debug = False
    go(app.run, host="::", port=9596)

    while True:
        logger.info("preparing next run...")
        scrape_start = time.time()
        data = json.load(open('activated_devices.json'))
        for item in data["devices"]:
            iccid = str(item["iccid"])
            iccid_q.put(iccid)

        jobs = iccid_q.qsize()

        logger.info("begin scraping (%d jobs to go)...", jobs)

        while len(content_buffers["upcoming"]) < jobs:
            time.sleep(1)

        scrape_end = time.time()
        scrape_took = scrape_end - scrape_start
        logger.info("done scraping (took %s)", str(timedelta(seconds=scrape_took)))

        content_buffers["upcoming"].append("scrape_duration %.2f" % scrape_took)

        content_buffers["active"] = content_buffers["upcoming"]
        content_buffers["upcoming"] = []

        time.sleep(3600*6 - scrape_took)

if __name__ == '__main__':
    main()
