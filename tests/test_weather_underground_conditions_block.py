from urllib.request import quote
from unittest.mock import patch
from requests import Response
from ..weather_underground_conditions_block import WeatherUndergroundConditions
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.modules.threading import Event


class WUnderTest(WeatherUndergroundConditions):
    def __init__(self, event):
        super().__init__()
        self._event = event

    def _process_response(self, resp):
        signals, paging = super()._process_response(resp)
        self._event.set()
        return signals, paging


class TestWeatherUndergroundConditions(NIOBlockTestCase):

    @patch("requests.get")
    @patch("requests.Response.json")
    def test_process_response(self, mock_json, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 200
        mock_json.return_value = {
            'current_observation': {
                'stuff': 'things'
            }
        }
        e = Event()
        blk = WUnderTest(e)
        city = 'San Francisco'
        state = 'California'
        self.configure_block(blk, {
            'polling_interval': {
                'seconds': 1
            },
            'retry_interval': {
                'seconds': 1
            },
            'queries': [{
                'state': state,
                'city': city
            }],
        })
        blk.start()
        e.wait(2)
        self.assert_num_signals_notified(1)
        self.assertEqual(mock_get.call_args[0][0],
                         blk.URL_FORMAT.format(
                             blk.api_key,
                             'conditions',
                             quote(state),
                             quote(city))
                         )
        blk.stop()
