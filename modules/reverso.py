import re

from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup

from config import LANGUAGES


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


_translator = Translator()


def _convert_to_markdown(element: str):
    return str(element).replace("<em>", "**").replace("</em>", "**")


def _parse_word(markdown_phrase: str):
    return re.findall(r"\*\*([^*]+)\*\*", markdown_phrase)


def _get_language(phrase: str):
    language = _translator.detect(phrase).lang
    return LANGUAGES[language]


class ReversoManager:
    def __init__(self, languages: tuple = ("испанский", "украинский")):
        self.languages = languages

        self.driver = webdriver.Chrome(options=options)
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def find_by_word(self, phrase: str, dest: str = "uk"):
        url = f"https://context.reverso.net/translation/{_get_language(phrase)}-{LANGUAGES[dest]}/{phrase}"
        print(url)
        self.driver.get(url)

        self.__press_close_window_button()

        example_content = self.driver.find_element(By.CSS_SELECTOR, "#examples-content")
        examples = example_content.find_elements(By.CLASS_NAME, "example")

        result = []

        for example in examples:
            html = example.get_attribute("outerHTML")
            soup = BeautifulSoup(html, "html.parser")

            src, dest = soup.find_all("span", class_="text")[:2]

            src = BeautifulSoup(_convert_to_markdown(src), "html.parser").text.strip()
            dest = BeautifulSoup(_convert_to_markdown(dest), "html.parser").text.strip()

            result.append({
                "src": {
                    "phrase": src,
                    "keyword": _parse_word(src)
                },
                "dest": {
                    "phrase": dest,
                    "keyword": _parse_word(dest)
                }
            })

        return result

    def __press_close_window_button(self):
        button = self.driver.find_element(By.CSS_SELECTOR, "#didomi-notice-agree-button")
        button.click()


if __name__ == "__main__":
    manager = ReversoManager(languages=("испанский", "украинский"))
    data = manager.find_by_word("tal vez")
    print(data)
