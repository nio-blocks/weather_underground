from nio.common.discovery import Discoverable, DiscoverableType
from .weather_underground_base import WeatherUndergroundBase


@Discoverable(DiscoverableType.block)
class WeatherUnderground(WeatherUndergroundBase):
    """ This block polls the Weather Underground API, grabbing the
    weather conditions in a given location.

    http://www.wunderground.com/weather/api/d/docs?d=data/conditions

    Params:
        queries (list): List of city/states to poll for weeather conds.

    """

    def __init__(self):
        super().__init__()
        self._api_endpoint = 'conditions'
        self._response_key = 'current_observation'
