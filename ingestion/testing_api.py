import requests
import json
from datetime import datetime

def test_fear_and_greed():
    url= "https://api.alternative.me/fng/?limit=1"
    try:
        response= requests.get(url)
        data= response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching Fear & Greed data: {e}")
        return None
if __name__=="__main__":
    data = test_fear_and_greed()
    if data:
        print("Fear & Greed API test successful!")
        print(data)
    else:
        print("Fear & Greed API test failed.")
  
