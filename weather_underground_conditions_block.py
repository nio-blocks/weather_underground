from nio.util.discovery import discoverable
from nio.properties.version import VersionProperty
from .weather_underground_base import WeatherUndergroundBase
from nio.signal.base import Signal


@discoverable
class WeatherUndergroundConditions(WeatherUndergroundBase):
    """ This block polls the Weather Underground API, grabbing the
    weather conditions in a given location.

    http://www.wunderground.com/weather/api/d/docs?d=data/conditions

    Params:
        city (string): City to poll for weather conds.
        state (string): State to poll for weather conds.

    """

    version = VersionProperty(version='2.0.0')

    def __init__(self):
        super().__init__()
        self._api_endpoint = 'conditions'

    def get_signal_from_response(self, resp):
        return Signal(resp.json().get('current_observation'))
