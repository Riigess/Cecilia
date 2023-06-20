# Cecilia
An easy-to-use Python-based RESTful API server designed to cache API requests, ambiguously deliver external API requests, and act as offline access to previously requested information in the event of a power outage or to be utilized during testing.

## Technologies used
- Python 3.10
- SQLite

## Libraries used
- pytest
- requests
- sqlite3
- flask
- flask-restful

## Development Operating Systems
- MacOS 12.0 (Monterey)
- Windows 11

## Why?
Long story short, a lot of development work has gone into pushing for generic APIs that you can use while connected to the internet. With power outages becoming ever more frequent, traveling returning to normal, and an interesting "what if" question, I figured why not develop a localized cache copy of a RESTful API that can update when you are back online.

To expand on all of that, power outages across the United States have become slightly more frequent (citing the massive rolling blackouts in Texas last year for residents) and with some devices becoming significantly more power efficient it makes sense that battery life may increase compared to their predecssors (yay). In my case, I have an M1 Max MacBook Pro that uses about 10w with a light load (VSCode and Terminal) and up to 65w under a heavy load (unreal engine 5), and a Desktop PC that uses about 50w idle and 500w under full load. The difference in power consumption between these two devices means that I can run with my MacBook for a few days (while only programming) without needing to connect the device to a charger of any sort, whereas the PC could use about the same power in...well...a dramatically sooner timespan with less work needed. That being said, in the event of a power outage and developers still need access to endpoints, it would suck to bog down cellular towers just so I can make queries to any external API. So, why not begin caching the outputs of those APIs and make it easier to access things when connected to the internet?

With that premise, Cecilia was started.
