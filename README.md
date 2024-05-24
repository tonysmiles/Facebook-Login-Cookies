# Facebook-Login-Cookies

<h2 id="authentication"> 🔐 Authentication</h2>

Authentication uses your browser's cookies. This workaround was done due to facebook's stricter stance on authentication by a Selenium-controlled browser.

Your `sessionid` is all that is required for authentication and can be passed as an argument to nearly any function

[🍪 Get cookies.txt](https://github.com/kairi003/Get-cookies.txt-LOCALLY) makes getting cookies in a [NetScape cookies format](http://fileformats.archiveteam.org/wiki/Netscape_cookies.txt).

After installing, open the extensions menu on [Facebook.com](https://facebook.com/) and click `🍪 Get cookies.txt` to reveal your cookies. Select `Export As ⇩` and specify a location and name to save.

Config.toml
```python
file_path = "D:/Python/AddFriendFacebook/cookies.txt"  
```

**Optionally**, `cookies_list` is a list of dictionaries with keys `name`, `value`, `domain`, `path` and `expiry` which allow you to pass your own browser cookies.

**Example:**

```python
cookies_list = [
    {
        'name': 'sessionid',
        'value': '**your session id**',
        'domain': 'https://facebook.com',
        'path': '/',
        'expiry': '03/2/2024, 12:18:58 PM'
    },
    # the rest of your cookies all in a list
]

```

<h2 id="browser-selection"> 👀 Browser Selection</h2>

[Google Chrome portable]([https://www.google.com/chrome](https://portableapps.com/apps/internet/google_chrome_portable)) is the preferred browser for **Facebooker**. The default anti-detection techniques used in this packaged are optimized for this. However, if you wish to use a different browser you may specify the `browser` in `upload_video` or `upload_videos`.

```python
from browsers import get_browser

driver = get_browser(name='chromeportable')
```

✅ Supported Browsers:

- **Chrome portable** (Recommended)
- **FireFox portable**
