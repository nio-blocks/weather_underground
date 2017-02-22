WeatherUnderground
===========

Polls [Weather Underground API](http://www.wunderground.com/weather/api/d/docs?d=data/conditions).

Creates a weather signal every *polling\_interval* for each location in *queries*.


Properties
--------------

-   **queries**: List of locations (city and state) to poll.
-   **api_key**: API credentials.
-   **polling_interval**: How often API is polled. When using more than one query. Each query will be polled at a period equal to the *polling\_interval* times the number of queries.
-   **retry_interval**: When a url request fails, how long to wait before attempting to try again.
-   **retry_limit**: When a url request fails, number of times to attempt a retry before giving up.


Dependencies
----------------

-   [requests](https://pypi.python.org/pypi/requests/)

Commands
----------------
None

Input
-------
None

Output
---------
One signal every *polling\_interval*. The signal has an attribute for every [Response Field](http://www.wunderground.com/weather/api/d/docs?d=data/conditions). The following is a list of commonly used attributes:

-   temp_f
-   temp_c
-   wind_dir
-   wind_mph
-   weather
-   icon_url
