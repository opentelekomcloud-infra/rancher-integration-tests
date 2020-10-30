import wrapt
from pyasli import BrowserSession, wait_for
from pyasli.bys import by_css, by_id, by_xpath
from pyasli.conditions import have_text, hidden, visible
from pyasli.elements.elements import Element, ElementCondition

from integration.tests.fields import Button, Field, TextInput


class Page:
    """Base page class bind to """

    url = NotImplemented

    def __init__(self, browser: BrowserSession):
        self.browser = browser

    def __getattribute__(self, item):
        value = super().__getattribute__(item)
        if isinstance(value, Field):
            value.__refresh__(self.browser)
        return value


@wrapt.decorator
def on_page(wrapped, instance=None, args=None, kwargs=None):
    """Run method only if current page is open"""
    if not isinstance(instance, Page):
        raise ValueError('`on_page` is only applicable to Page fields')
    if instance.browser.url != instance.url:
        raise AssertionError('Page URL mismatch: expected')
    return wrapped(*args, **kwargs)


def requires_visible(locator, timeout=10):
    """Run method only after required element becomes visible"""

    @wrapt.decorator
    def _requires_visible(wrapped, instance=None, args=None, kwargs=None):
        if not isinstance(instance, Page):
            raise ValueError('`requires_visible` is only applicable to Page fields')
        instance.browser.element(locator).assure(visible, timeout)
        return wrapped(*args, **kwargs)

    return _requires_visible


def requires_hidden(locator, timeout=10):
    """Run method only after required element becomes visible"""

    @wrapt.decorator
    def _requires_hidden(wrapped, instance=None, args=None, kwargs=None):
        if not isinstance(instance, Page):
            raise ValueError('`requires_hidden` is only applicable to Page fields')
        instance.browser.element(locator).assure(hidden, timeout)
        return wrapped(*args, **kwargs)

    return _requires_hidden


class LoginPage(Page):
    url = '/login'

    _username = TextInput(by_id('login-username-local'))
    _password = TextInput(by_id('login-password-local'))
    _sign_in = Button(by_css('button.bg-primary'))

    @on_page
    def login(self, next_url, username, password):
        """Login user and open URL

        :param str next_url: Target page url
        :param str username: Rancher user name
        :param str password: Rancher password
        """
        self.browser.open(next_url)
        self._username.input(username)
        self._password.text = password
        self._sign_in.click()
        wait_for(self.browser, lambda b: b.url == next_url, timeout=10)


class ClusterListPage(Page):
    url = '/n/drivers/cluster'

    _add_driver = Button(by_xpath(r"//button[contains(., 'Add Cluster Driver')]"))

    @on_page
    def click_add_cluster_driver(self):
        self._add_driver.click()

    # register dialog

    _download_url = TextInput(by_xpath(r"//div[contains(., 'Download URL')]/input"))
    _custom_ui_url = TextInput(by_xpath(r"//div[contains(., 'Custom UI URL')]/input"))
    _add_domain = Button(by_xpath(r"//span[contains(., 'Add Domain')]"))
    _domain = TextInput(by_xpath(r"//div[contains(., 'Whitelist Domains')]//input"))
    _create = Button(by_xpath(r"//button[contains(., 'Create')]"))

    @requires_visible(by_css('form.modal-container.large-modal'))
    def register_driver(self, url, ui_url, allowed_domain=''):
        """Register new cluster driver"""
        self._download_url.input(url)
        self._custom_ui_url.input(ui_url)
        if allowed_domain:
            self._add_domain.click()
            self._domain.input(allowed_domain)
        self._create.click()

    # table
    _otccce_line = Field(by_xpath(r"//tr[contains(.,'kontainer-engine-driver-otccce')]"))

    @requires_hidden(by_css('form.modal-container.large-modal'))
    def wait_for_activation(self):
        """Wait for driver to become 'Active'"""
        span = by_css('span.badge-state')
        wait_for(self._otccce_line, _have_subelement_with_text(span, 'Activating'), 60)
        wait_for(self._otccce_line, _have_subelement_with_text(span, 'Active'), 60)


def _have_subelement_with_text(locator, text) -> ElementCondition:
    def _condition(elem: Element):
        return elem.element(locator).should(have_text(text))

    return _condition
