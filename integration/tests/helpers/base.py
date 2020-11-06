import wrapt
from pyasli import BrowserSession
from pyasli.bys import CssSelectorOrBy
from pyasli.conditions import exist
from pyasli.elements import Element


class Field:
    """Class for describing fields in class

    Wraps :class:`Element`

    Fields can have other fields inside
    """

    _locator: CssSelectorOrBy
    _base: Element = None

    def __get__(self, instance, owner):
        """Work as descriptor"""
        if isinstance(instance, Field):
            searcher = instance._base
        elif isinstance(instance, Page):
            searcher = instance.browser
        else:
            raise TypeError(f"Can't use `Field` as attribute of class {owner}")
        self.__refresh__(searcher)
        return self

    def __getattribute__(self, item):
        """Handle child fields with care"""
        val = super().__getattribute__(item)
        if isinstance(val, Field):
            val.__refresh__(self._base)
        return val

    def __getattr__(self, item):
        """For missing attributes search in wrapped element"""
        return getattr(self._base, item)

    def __init__(self, locator: CssSelectorOrBy):
        self._locator = locator

    def _move_to(self):
        self._base.assure(exist)
        return self._base.get_actual().location_once_scrolled_into_view

    def __refresh__(self, searcher):
        """Method to update element reference if it is already dead"""
        if self._base is None:
            self._base = searcher.element(self._locator)
        return self._base

    def sub_element(self, locator):
        """Find sub-element of the field"""
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


class Page:
    """Base page class"""

    url = NotImplemented

    def __init__(self, browser: BrowserSession):
        self.browser = browser

    def open(self):
        return self.browser.open(self.url)


@wrapt.decorator
def on_page(wrapped, instance=None, args=None, kwargs=None):
    """Run method only if current page is open"""
    if not isinstance(instance, Page):
        raise ValueError('`on_page` is only applicable to Page fields')
    if instance.browser.url != instance.url:
        raise AssertionError(f'Page URL mismatch. Expected {instance.url},'
                             f'got {instance.browser.url}')
    return wrapped(*args, **kwargs)
