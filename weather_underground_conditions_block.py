from nio.util.discovery import discoverable
from nio.properties.version import VersionProperty
from .weather_underground_base import WeatherUndergroundBase


@discoverable
class WeatherUndergroundConditions(WeatherUndergroundBase):
    """ This block polls the Weather Underground API, grabbing the
    weather conditions in a given location.

    http://www.wunderground.com/weather/api/d/docs?d=data/conditions

    Params:
        queries (list): List of city/states to poll for weeather conds.

    """

    version = VersionProperty(version='1.0.0')

    def __init__(self):
        super().__init__()
        self._api_endpoint = 'conditions'
        self._response_key = 'current_observation'
