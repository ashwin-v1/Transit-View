import requests
import pandas as pd
from google.transit import gtfs_realtime_pb2

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
DATASET_ID = "ttc-bustime-real-time-next-vehicle-arrival-nvas"
VEHICLE_FEED_URL = "https://bustime.ttc.ca/gtfsrt/vehicles"

def fetch_ttc_data(limit: int = 500) -> pd.DataFrame:

    package_url = f"{BASE_URL}/api/3/action/package_show"
    package = requests.get(package_url, params={"id": DATASET_ID}).json()
    resources = [r for r in package["result"]["resources"] if r["datastore_active"]]

    if not resources:
        return pd.DataFrame()

    resource_id = resources[0]["id"]
    data_url = f"{BASE_URL}/api/3/action/datastore_search"
    params = {"resource_id": resource_id, "limit": limit}
    data = requests.get(data_url, params=params).json()
    records = data["result"]["records"]
    df = pd.DataFrame(records)
    return df

def get_vehicle_data():
    try:
   
        feed = gtfs_realtime_pb2.FeedMessage()
        
        
        response = requests.get(VEHICLE_FEED_URL)
        response.raise_for_status() 

        feed.ParseFromString(response.content)

        vehicles = []
        for entity in feed.entity:
            if entity.HasField('vehicle'):
                v = entity.vehicle
                if v.position.latitude == 0.0 and v.position.longitude == 0.0:
                    continue  
                vehicles.append({
                    "id": v.vehicle.id,
                    "latitude": v.position.latitude,
                    "longitude": v.position.longitude,
                    "route": v.trip.route_id,
                    "stop_id": v.stop_id,
                    "current_status": v.current_status
                })
        return {"vehicles": vehicles}
    
    except Exception as e:
        return {"error": str(e)}