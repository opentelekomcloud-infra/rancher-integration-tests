import random

from pyasli.bys import by_xpath
from pyasli.conditions import clickable, exist, text_is
from selenium.common.exceptions import WebDriverException

from integration.tests.helpers.base import Field


class TextInput(Field):
    """Text input element"""

    def __get__(self, instance, owner) -> 'TextInput':
        """This is typing stub"""
        return super().__get__(instance, owner)

    def input(self, text):
        """Replace current field value with given"""
        self._base.assure(exist)
        self._move_to()
        self._base.assure(clickable)
        self._base.click()
        self._base.text = text


class Button(Field):
    """Button element"""

    def __get__(self, instance, owner) -> 'Button':
        """This is typing stub"""
        return super().__get__(instance, owner)

    def click(self):
        """Click the button"""
        self._move_to()
        self._base.assure(clickable)
        self._base.click()


class SearchSelect(Field):
    """Container with text input and lines"""

    def __init__(self, xpath):
        """Searchable select `EmberJS` field

        :param str xpath: base element xpath
        """
        super().__init__(by_xpath(xpath))
        self._base_xpath = xpath
        self._text_input = TextInput(by_xpath(xpath + r'//input[@type="text"]'))

    @property
    def lines(self):
        return self._base.browser.elements(
            by_xpath(self._base_xpath + r'//div[@class="searchable-option"]'))

    def select(self, text, index=0):
        """Select item from list by index after entering some text"""

        try:
            self._text_input.input(text)
            self.lines[index].click()
        except WebDriverException as wde:
            screenshot = self._base.browser.get_actual().get_screenshot_as_png()
            png_path = f'logs/select-fail-{random.randrange(0xffffff):06x}.png'
            with open(png_path, 'wb+') as png:
                png.write(screenshot)
            raise Exception(f'Failed to select item.\nScreenshot: {png_path}') from wde


class _StateField(Field):
    _css_selector = 'td.state'

    def __init__(self):
        super().__init__(_StateField._css_selector)

    def assure(self, value, timeout=60):
        super().assure(text_is(value), timeout)


class ClusterRow(Field):

    def __init__(self, cluster_name):
        self._base_xpath = f'//tr[./td/a[text()="{cluster_name}"]]'
        super().__init__(by_xpath(self._base_xpath))

    state = _StateField()

    def to_details(self):
        child_xpath = r'/td[contains(@data-title, "Cluster Name")]/a'
        edit_link = self._base.browser.element(by_xpath(self._base_xpath + child_xpath))
        edit_link.click()


class ClusterDriverRow(Field):

    def __init__(self, url_text):
        self._base_xpath = f'//tr[./td[contains(.,"{url_text}")]]'
        super().__init__(by_xpath(self._base_xpath))

    state = _StateField()
