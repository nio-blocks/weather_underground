from nio.common.discovery import Discoverable, DiscoverableType
from .weather_underground_base import WeatherUndergroundBase


@Discoverable(DiscoverableType.block)
class WeatherUndergroundForecast10Day(WeatherUndergroundBase):
    """ This block polls the Weather Underground API, grabbing the
    weather forecast10day in a given location.

    http://www.wunderground.com/weather/api/d/docs?d=data/forecast10day&MR=1

    Params:
        queries (list): List of city/states to poll for weeather conds.

    """

    def __init__(self):
        super().__init__()
        self._api_endpoint = 'forecast10day'
        self._response_key = 'forecast'
