import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
# Webdriver managers
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium_stealth import stealth
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver

# Ensure the correct path to the main Firefox executable
FIREFOX_BINARY_PATH = r'E:\Firefox\Chờ\ChiboOfficial\App\Firefox64\firefox.exe'
# Path to the Firefox profile
FIREFOX_PROFILE_PATH = r'E:\Firefox\Chờ\ChiboOfficial\Data\profile'

CHROME_BINARY_PATH = r'C:\Users\tuanm\OneDrive\Máy tính\Chrome\Goc\App\Chrome-bin\Chrome.exe'
CHROME_PROFILE_PATH = r'C:\Users\tuanm\OneDrive\Máy tính\Chrome\Goc\Data\profile'

def get_firefox_portable_browser(options=None, user_agent=None , *args, **kwargs) -> webdriver:
    """
    Run Firefox Portable with pre-configured proxy profile
    """
    if not os.path.isfile(FIREFOX_BINARY_PATH):
        print(f"Invalid path or file does not exist: {FIREFOX_BINARY_PATH}")
        return None

    if not os.path.isdir(FIREFOX_PROFILE_PATH):
        print(f"Invalid path or profile does not exist: {FIREFOX_PROFILE_PATH}")
        return None

    options = options or firefox_defaults(headless=False)
    options.binary_location = FIREFOX_BINARY_PATH  # Set the path to the main Firefox executable

    # Use the pre-configured proxy profile
    options.add_argument(f'-profile')
    options.add_argument(FIREFOX_PROFILE_PATH)

    # Customize User-Agent
    if user_agent:
        options.set_preference("general.useragent.override", user_agent)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)

    try:
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        # Customize JavaScript to hide Selenium
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32',
            });
            Object.defineProperty(navigator, 'vendor', {
                get: () => 'Google Inc.',
            });
            window.navigator.chrome = {
                runtime: {},
            };
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)

        print("Firefox Portable started successfully")
        return driver
    except Exception as e:
        print(f"Error starting Firefox Portable: {e}")
        return None

def get_chrome_portable_browser(options=None, user_agent=None , *args, **kwargs) -> webdriver:
    """
    Run Chrome Portable with pre-configured proxy profile
    """
    if not os.path.isfile(CHROME_BINARY_PATH):
        print(f"Invalid path or file does not exist: {CHROME_BINARY_PATH}")
        return None

    if not os.path.isdir(CHROME_PROFILE_PATH):
        print(f"Invalid path or profile does not exist: {CHROME_PROFILE_PATH}")
        return None

    options = options or chrome_defaults(headless=False)
    options.binary_location = CHROME_BINARY_PATH  # Set the path to the main Chrome executable

    # Use the pre-configured proxy profile
    options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')

    # Customize User-Agent
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')

    try:
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Customize JavaScript to hide Selenium
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        print("Chrome Portable started successfully")
        return driver
    except Exception as e:
        print(f"Error starting Chrome Portable: {e}")
        return None

def get_browser(name: str = 'chrome', options=None, user_agent: str = None) -> webdriver:
    """
    Get the browser based on the name with the ability to pass additional arguments
    """
    if name.lower() == 'chromeportable':
        return get_chrome_portable_browser(options, user_agent)
    elif name.lower() == 'firefoxportable':
        return get_firefox_portable_browser(options, user_agent)
    elif name.lower() == 'chrome':
        options = options or chrome_defaults()
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    else:
        raise UnsupportedBrowserException(f"Browser '{name}' is not supported.")

def get_driver(name: str = 'chrome', *args, **kwargs) -> webdriver:
    """
    Get the WebDriver function for the browser
    """
    if _clean_name(name) in drivers:
        return drivers[name]

    raise UnsupportedBrowserException()

def get_service(name: str = 'chrome'):
    """
    Get the service to install the browser driver according to webdriver-manager documentation

    https://pypi.org/project/webdriver-manager/
    """
    if _clean_name(name) in services:
        return services[name]()

    return None  # Safari does not require a service

def get_default_options(name: str, *args, **kwargs):
    """
    Get default options for each browser to help maintain anonymity
    """
    name = _clean_name(name)

    if name in defaults:
        return defaults[name](*args, **kwargs)

    raise UnsupportedBrowserException()

def chrome_defaults(*args, headless: bool = False, proxy: dict = None, user_agent: str = None, **kwargs) -> ChromeOptions:
    """
    Create Chrome with options
    """
    options = ChromeOptions()

    # General settings
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--profile-directory=Default')

    # Experimental settings
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    # Add English language to avoid language translation errors
    options.add_argument("--lang=en")

    # Disable WebRTC
    options.add_argument('--disable-webrtc')

    # Set custom User-Agent if provided
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')

    # Headless mode
    if headless:
        options.add_argument('--headless=new')

    return options

def firefox_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> FirefoxOptions:
    """
    Create Firefox with default options
    """
    options = FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    if proxy:
        raise NotImplementedError('Proxy support is not implemented for this browser')
    return options

def safari_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> SafariOptions:
    """
    Create Safari with default options
    """
    options = SafariOptions()

    # Default options

    if headless:
        options.add_argument('--headless')
    if proxy:
        raise NotImplementedError('Proxy support is not implemented for this browser')
    return options

def edge_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> EdgeOptions:
    """
    Create Edge with default options
    """
    options = EdgeOptions()

    # Default options

    if headless:
        options.add_argument('--headless')
    if proxy:
        raise NotImplementedError('Proxy support is not implemented for this browser')
    return options

# Misc
class UnsupportedBrowserException(Exception):
    """
    Browser not supported by the library

    Supported browsers:
        - Chrome
        - Firefox
        - Safari
        - Edge
    """

    def __init__(self, message=None):
        super().__init__(message or self.__doc__)

def _clean_name(name: str) -> str:
    """
    Clean the name of the browser for easier use
    """
    return name.strip().lower()

drivers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'safari': webdriver.Safari,
    'edge': webdriver.Edge,
}

defaults = {
    'chrome': chrome_defaults,
    'firefox': firefox_defaults,
    'safari': safari_defaults,
    'edge': edge_defaults,
}

services = {
    'chrome': lambda: ChromeService(ChromeDriverManager().install()),
    'firefox': lambda: FirefoxService(GeckoDriverManager().install()),
    'edge': lambda: EdgeService(EdgeChromiumDriverManager().install()),
}
