import requests
from requests.structures import CaseInsensitiveDict
import json
print("Fetcher for github actions")
def refresh_busstops():
    print("Refresh Busstops")
    url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"
    response = requests.get(url)
    tmp = response.json()
    stops={}
    for t in tmp["data"]:
        stops[t["stop"]]={"chi":t["name_tc"],"eng":t["name_en"]}
    print("Completed Count.")
    with open("stops.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(stops, indent = 4) 
        file.write(json_object)
STOPSINFO={}
INBOUND={}
OUTBOUND={}
def getallroute():
    url = "https://data.etabus.gov.hk/v1/transport/kmb/route-stop"
    response = requests.get(url)
    tmp = response.json()
    stops={}
    stops2={}
    for t in tmp["data"]:
        print(f"Fetching Data, Route:{t["route"]}.....")
        if t["bound"] == "O":
            if t["route"] not in stops:
                stops[t["route"]]=[]
            stops[t["route"]].append([t["stop"],t["service_type"]])
        else:
            if t["route"] not in stops2:
                stops2[t["route"]]=[]
            stops2[t["route"]].append([t["stop"],t["service_type"]])
    with open("outbound.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(stops, indent = 4) 
        file.write(json_object)
    with open("inbound.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(stops2, indent = 4) 
        file.write(json_object)
def citybus_refresh():
    url = "https://rt.data.gov.hk/v1/transport/citybus-nwfb/route/ctb"
    response = requests.get(url)
    tmp = response.json()
    routes=[]
    for t in tmp["data"]:
        routes.append(t["route"])
    rr={}
    rr2={}
    stations=[]
    for route in routes:
        print(f"Feching Route: {route}...")
        url = f"https://rt.data.gov.hk/v1/transport/citybus-nwfb/route-stop/ctb/{route}/outbound"
        response = requests.get(url)
        tmp = response.json()
        for t in tmp["data"]:
            if route not in rr:
                rr[route]=[]
            else:
                rr[route].append(t["stop"])
            if t["stop"] not in stations:
                stations.append(t["stop"])
        print(f"Feching Route2: {route}...")
        url = f"https://rt.data.gov.hk/v1/transport/citybus-nwfb/route-stop/ctb/{route}/inbound"
        response = requests.get(url)
        tmp = response.json()
        for t in tmp["data"]:
            if route not in rr2:
                rr2[route]=[]
            else:
                rr2[route].append(t["stop"])
            if t["stop"] not in stations:
                stations.append(t["stop"])
    with open("outbound_2.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(rr, indent = 4) 
        file.write(json_object)
    with open("inbound_2.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(rr2, indent = 4) 
        file.write(json_object)
    with open("rr_stations.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(stations, indent = 4) 
        file.write(json_object)
def cb():
    with open("rr_stations.json",encoding="UTF-8") as file:
        cba=json.loads(file.read())
    d={}
    for a in cba:
        url=f"https://rt.data.gov.hk/v1/transport/citybus-nwfb/stop/{a}"
        response = requests.get(url)
        tmp = response.json()
        d[a]={"chi":tmp['data']["name_tc"],"eng":tmp['data']["name_en"]}
        print(f"Got station: {tmp['data']['name_en']}")
    with open("ttt.json","w",encoding="UTF-8") as file:
        json_object = json.dumps(d, indent = 4) 
        file.write(json_object)
refresh_busstops()
getallroute()
citybus_refresh()
cb()
print("Refresh Complete - Data Updated")
