from urllib.request import quote
from nio.common.discovery import Discoverable, DiscoverableType
from .http_blocks.rest.rest_block import RESTPolling
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.object import ObjectProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.metadata.properties.timedelta import TimeDeltaProperty
from nio.common.signal.base import Signal
from datetime import timedelta


class Location(PropertyHolder):
    state = StringProperty(title='State')
    city = StringProperty(title='City')


class WeatherUndergroundBase(RESTPolling):
    """ This base block polls the Weather Underground API.

    Blocks that extend this should specify the api endpoint and what to extract
    from the response. This base block uses 'conditions' as an example:
        http://www.wunderground.com/weather/api/d/docs?d=data/conditions

    Params:
        queries (list): List of city/states to poll for weeather conds.

    """
    URL_FORMAT = ("http://api.wunderground.com/api/{}/"
                  "{}/q/{}/{}.json")

    queries = ListProperty(Location, title='Locations')
    api_key = StringProperty(title='API Key',
                             default='[[WEATHER_UNDERGROUND_KEY_ID]]')
    polling_interval = TimeDeltaProperty(title='Polling Interval',
                                         default=timedelta(seconds=300))
    retry_interval = TimeDeltaProperty(title='Retry Interval',
                                       default=timedelta(seconds=10))

    def __init__(self):
        super().__init__()
        self._api_endpoint = 'conditions'
        self._response_key = 'current_observation'

    def configure(self, context):
        super().configure(context)

    def _process_response(self, resp):
        """ Extract weather conditions from response.

        Args:
            resp (Response)

        Returns:
            signals (list(Signal)): List containing one weather signal.
            paging (bool): Always false because we do not feed to page.

        """
        signals = []
        paging = False
        resp = resp.json()
        data = resp.get(self._response_key)

        if data:
            signals = [Signal(data)]
            self._logger.debug(
                "Creating weather undergrond signal for: {0},{1}"
                .format(self.current_query.city, self.current_query.state)
            )
        else:
            self._logger.warning(
                "Failed getting weather for: {0},{1}"
                .format(self.current_query.city, self.current_query.state)
            )

        return signals, paging

    def _prepare_url(self, paging=False):
        """ Overridden from RESTPolling block.

        Args:
            paging (bool): Are we paging?

        Returns:
            headers (dict): Contains the (case sensitive) http headers.

        """
        headers = {"Content-Type": "application/json"}
        self.url = self.URL_FORMAT.format(self.api_key,
                                          self._api_endpoint,
                                          quote(self.current_query.state),
                                          quote(self.current_query.city))

        return headers

    @property
    def current_query(self):
        return self.queries[self._idx]
