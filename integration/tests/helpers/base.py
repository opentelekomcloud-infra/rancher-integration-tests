from __future__ import annotations

import wrapt
from pyasli import BrowserSession
from pyasli.bys import CssSelectorOrBy
from pyasli.elements import Element
from pyasli.elements.elements import FindElementsMixin


class _Wrapper(FindElementsMixin):
    """Base for Page and Field"""

    _base: FindElementsMixin

    def element(self, by: CssSelectorOrBy):
        return self._base.element(by)

    def elements(self, by: CssSelectorOrBy):
        return self._base.elements(by)


class Page(_Wrapper):
    """Base page class"""

    url = NotImplemented
    _base: BrowserSession

    def __init__(self, browser: BrowserSession):
        self._base = browser

    @property
    def browser(self):
        return self._base

    def open(self):
        return self._base.open(self.url)

    def is_current(self):
        return self._base.url == self.url


@wrapt.decorator
def on_page(wrapped, instance=None, args=None, kwargs=None):
    """Run method only if current page is open"""
    if not isinstance(instance, Page):
        raise ValueError('`on_page` is only applicable to Page fields')
    if not instance.is_current:
        raise AssertionError(f'Page URL mismatch. Expected {type(instance).url},'
                             f'got {instance.browser.url.url}')
    return wrapped(*args, **kwargs)


class Field(_Wrapper):
    """Element wrapper

    Narrows Element functionality
    """

    _base: Element

    def __init__(self, locator: CssSelectorOrBy, parent: _Wrapper):
        self._locator = locator
        self._parent = parent
        self._base = self._parent.element(self._locator)

    def assure(self, condition, timeout=20):
        """Assure wrapped element state

        :raises TimeoutError:
        """
        return self._base.assure(condition, timeout)

    def should(self, condition, timeout=20):
        """Check wrapped element state

        :raises AssertionError:
        """
        return self._base.should(condition, timeout)

    should_be = should

    def __getattr__(self, item):
        """For missing attributes search in wrapped element"""
        return getattr(self._base, item)


class _FieldDescriptor:
    """Descriptor returning ``Field`` with given class and locator"""

    def __init__(self, locator: CssSelectorOrBy, field_cls: type = Field):
        self._locator = locator
        self._cls = field_cls

    def __set_name__(self, owner, name):
        self._name = f'_field_{name}'

    def __get__(self, instance, owner):
        """Lazy field loading"""
        if not hasattr(instance, self._name) or \
                getattr(instance, self._name) is None:
            # None is special case for Field
            # workflow for missing attr there:
            # Field.__getattr__ -> Element.__getattr__ ->
            # -> Element.get_attribute(...) -> WebElement.get_attribute(...)
            value = self._cls(self._locator, instance)
            setattr(instance, self._name, value)
        return getattr(instance, self._name)


def field(locator: CssSelectorOrBy, cls: type = Field):
    """Lazy field descriptor"""
    return _FieldDescriptor(locator, cls)
