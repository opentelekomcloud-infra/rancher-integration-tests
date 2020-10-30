from pyasli.bys import CssSelectorOrBy
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
