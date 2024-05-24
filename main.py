import json
import toml
from auth import AuthBackend
from browsers import get_browser
from utils import green, red

config = toml.load('config.toml')


def load_links(filename="data.json"):
    with open(filename, "r") as file:
        data = json.load(file)
    return data["links"]


def save_links(links, filename="data.json"):
    with open(filename, "w") as file:
        json.dump({"links": links}, file, indent=4)


def main():
    links = load_links()

    driver = get_browser(name='chromeportable')

    if driver is None:
        print("Unable to initialize browser")
        return

    auth = AuthBackend(cookies=config['cookies']['file_path'])
    auth.authenticate_agent(driver)
    driver.get(config['paths']['main'])

    try:
        driver.find_element("xpath", "//span[text()='Photos/videos']")
        print(green("Logged in successfully!"))
    except Exception as e:
        print(red("Login failed:", e))


    if config['quit_on_end']:
        driver.quit()


if __name__ == "__main__":
    main()
