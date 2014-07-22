from urllib.request import quote
from nio.common.discovery import Discoverable, DiscoverableType
from .http_blocks.rest.rest_block import RESTPolling
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.object import ObjectProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.common.signal.base import Signal


class WeatherUndergroundSignal(Signal):
    def __init__(self, data):
        for k in data:
            setattr(self, k, data[k])


class Location(PropertyHolder):
    state = StringProperty(title='State')
    city = StringProperty(title='City')


@Discoverable(DiscoverableType.block)
class WeatherUnderground(RESTPolling):
    """ This block polls the Weather Underground API, grabbing the
    weather conditions in a given location.

    Params:
        queries (list): List of city/states to poll for weeather conds.

    """
    URL_FORMAT = ("http://api.wunderground.com/api/{0}/"
                  "conditions/q/{1}/{2}.json")

    queries = ListProperty(Location, title='Locations')
    api_key = StringProperty(title='API Key')

    def __init__(self):
        super().__init__()

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
        data = resp.get('current_observation')

        if data:
            signals = [WeatherUndergroundSignal(data)]
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
                                          quote(self.current_query.state),
                                          quote(self.current_query.city))

        return headers

    @property
    def current_query(self):
        return self.queries[self._idx]
