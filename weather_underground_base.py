import requests
from urllib.request import quote
from nio.block.base import Block
from nio.util.discovery import  not_discoverable
from nio.properties.list import ListProperty
from nio.properties.string import StringProperty
from nio.properties.holder import PropertyHolder
from nio.properties.timedelta import TimeDeltaProperty
from nio.signal.base import Signal
from datetime import timedelta


@not_discoverable
class WeatherUndergroundBase(Block):
    """ This base block polls the Weather Underground API.

    Blocks that extend this should specify the api endpoint and what to extract
    from the response. This base block uses 'conditions' as an example:
        http://www.wunderground.com/weather/api/d/docs?d=data/conditions

    Params:
        queries (list): List of city/states to poll for weeather conds.

    """
    URL_FORMAT = ("http://api.wunderground.com/api/{}/"
                  "{}/q/{}/{}.json")

    state = StringProperty(title='State', default='')
    city = StringProperty(title='City', default='')
    api_key = StringProperty(title='API Key',
                             default='[[WEATHER_UNDERGROUND_KEY_ID]]')

    def __init__(self):
        super().__init__()
        self._api_endpoint = 'conditions'

    def configure(self, context):
        super().configure(context)

    def process_signals(self, signals):
        response = None
        weather_signals = []

        for signal in signals:
            response = self.get_weather_from_city_state(
                            self.state(signal),
                            self.city(signal))
            weather_signals.append(Signal(response.json()))

        self.notify_signals(weather_signals)

    def get_weather_from_city_state(self, state, city):
        """ Execute the request

        """
        headers = {"Content-Type": "application/json"}
        resp = None
        self.url = self.URL_FORMAT.format(self.api_key(),
                                          self._api_endpoint,
                                          state,
                                          city)

        try:
            resp = requests.get(self.url, headers=headers)
            if resp.status != 200:
                self.logger.warning("GET request returned response status {}"
                    .format(resp.status))
        except:
            self.logger.exception("GET request failed")
        finally:
            return resp
