import requests

class WeatherAPI:
    def __init__(self, 
                 latitude: str, 
                 longitude: str,
                 units: str = "e",
                 language: str = "en-US",
                 format: str = "json",
                 apiKey: str = "71f92ea9dd2f4790b92ea9dd2f779061"
                 ):
        
        if not (-90 <= float(latitude) <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= float(longitude) <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        
        if any(param is None or param == "" for param in [units, language, format, apiKey]):
            raise ValueError("Units, language, format, or apiKey cannot be None or empty strings.")
        
        self.latitude = latitude
        self.longitude = longitude
        self.units = units
        self.language = language
        self.format = format
        self.apiKey = apiKey
        
        self.lat_long = f"{self.latitude},{self.longitude}"
        
        self.parameters = {
            "geocode": self.lat_long,
            "units": self.units,
            "language": self.language,
            "format": self.format,
            "apiKey": self.apiKey
        }
        
        self.base_url = "https://api.weather.com/v3/wx"

    def __repr__(self):
        return f"WeatherAPI(latitude={self.latitude}, longitude={self.longitude}, units={self.units}, language={self.language}, format={self.format}, apiKey={self.apiKey})"
    
    def _build_request_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint}"

    def _make_get_request(self, endpoint: str):
        url = self._build_request_url(endpoint)
        response = requests.get(url, params=self.parameters)
        response.raise_for_status()
        return response.json()
    
    def get_current_weather(self):
        return self._make_get_request("observations/current")
    
    def get_2_day_hourly_forecast(self):
        return self._make_get_request("forecast/hourly/2day")
    
    def get_3_day_daily_forecast(self):
        return self._make_get_request("forecast/daily/3day")
    
    def get_7_day_daily_forecast(self):
        return self._make_get_request("forecast/daily/7day")
    
    
    def get_15_minute_forecast(self):
        return self._make_get_request("forecast/fifteenminute")