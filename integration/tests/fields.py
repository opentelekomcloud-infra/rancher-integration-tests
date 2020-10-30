from pyasli.bys import CssSelectorOrBy, by_xpath
from pyasli.conditions import exist, visible
from pyasli.elements import Element


class Field:
    """Class for describing fields in class. Wraps :class:`Element`"""

    _locator: CssSelectorOrBy
    _base: Element = None

    def __init__(self, locator: CssSelectorOrBy):
        self._locator = locator

    def __refresh__(self, browser):
        """Method to update browser reference if it is already dead"""
        if (self._base is None) or (self._base.browser != browser):
            self._base = browser.element(self._locator)
        return self._base

    def sub_element(self, locator):
        """Find subelement if the field"""
        return self._base.element(locator)

    def assure(self, condition, timeout=5):
        """Assure wrapped element state

        :raises TimeoutError:
        """
        return self._base.assure(condition, timeout)

    def should(self, condition, timeout=5):
        """Check wrapped element state

        :raises AssertionError:
        """
        return self._base.should(condition, timeout)

    should_be = should


class TextInput(Field):
    """Text input element"""

    def input(self, text):
        """Replace current field value with given"""
        self._base.assure(exist)
        self._base.assure(visible)
        self._base.click()
        self._base.text = text


class Button(Field):
    """Button element"""

    def click(self):
        """Click the button"""
        self._base.click()


def enabled(element: Element):
    """Condition for checking if element is not disabled"""
    return element.enabled


def disabled(element: Element):
    """Condition for checking if element is disabled"""
    return element.disabled


class SearchableSelect(Field):
    """Container with text input and lines"""

    def __init__(self, base_xpath):
        super().__init__(by_xpath(base_xpath))
        self.text_input = TextInput(
            by_xpath(base_xpath + r'//input[@type="text"]'))
        self.lines = self._base.elements(
            by_xpath(base_xpath + r'//div[@class="searchable-option"]'))

    def select(self, text, index):
        """Select item from list by index after entering some text"""
        self.text_input.input(text)
        self.lines[index].click()
