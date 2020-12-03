import logging
import random

from pyasli.bys import by_xpath
from pyasli.conditions import clickable, exist, text_is, visible
from selenium.common.exceptions import WebDriverException

from integration.tests.helpers.base import Field, field

LOGGER = logging.getLogger('helpers.fields')


class TextInput(Field):
    """Text input element"""

    def input(self, text):
        """Replace current field value with given"""
        self._base.assure(exist)
        self._base.assure(visible)
        self._base.move_to()
        self._base.assure(clickable)
        self._base.click()
        self._base.text = text
        LOGGER.debug('Entered text "%s" into %s', text, self._base)

    @property
    def text(self):
        """Return field text value"""
        return self._base.value


def text_input(locator) -> TextInput:
    """Lazy TextInput loader"""
    return field(locator, TextInput)


class Button(Field):
    """Button element"""

    def click(self):
        """Click the button"""
        self._base.move_to()
        self._base.assure(clickable)
        self._base.click()
        LOGGER.debug('Clicked button %s', self._base)


def button(locator) -> Button:
    """Lazy Button loader"""
    return field(locator, Button)


class SearchSelect(Field):
    """Container with text input and lines"""

    _text_input = text_input('input[type=text]')

    @property
    def lines(self):
        return self._base.elements('div.searchable-option')

    def select(self, text, index=0):
        """Select item from list by index after entering some text"""

        try:
            self._text_input.input(text)
            self.lines[index].click()
            LOGGER.debug('Selected item #%d by text "%s"', index, text)
        except WebDriverException as wde:
            screenshot = self._base.browser.get_actual().get_screenshot_as_png()
            png_path = f'logs/select-fail-{random.randrange(0xffffff):06x}.png'
            with open(png_path, 'wb+') as png:
                png.write(screenshot)
            raise Exception(f'Failed to select item.\nScreenshot: {png_path}') from wde


def search_select(locator) -> SearchSelect:
    """Ember searchable-select"""
    return field(locator, SearchSelect)


class _StateField(Field):

    def assure(self, value, timeout=60):
        return super().assure(text_is(value), timeout)


def _state_field(locator) -> _StateField:
    return field(locator, _StateField)


class Row(Field):
    """Single cluster/driver row"""
    state = _state_field('td.state')
    more_actions = button('div.more-actions')


def cluster_driver_row(url) -> Row:
    return field(by_xpath(f'//tr[./td[contains(., "{url}")]]'), Row)


def cluster_row(name, parent) -> Row:
    """NB! this is not a descriptor, but an actual Row"""
    return Row(by_xpath(f'//tr[./td/a[text()="{name}"]]'), parent)
