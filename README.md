WeatherUnderground
===========

Polls [Weather Underground API](http://www.wunderground.com/weather/api/d/docs?d=data/conditions).

Creates a weather signal every *polling\_interval* for each location in *queries*.


Properties
--------------

-   **city**: City to poll.
-   **state**: State to poll.
-   **api_key**: API credentials.


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
