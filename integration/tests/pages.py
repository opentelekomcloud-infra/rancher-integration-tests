import wrapt
from pyasli import BrowserSession, wait_for
from pyasli.bys import by_css, by_id, by_xpath
from pyasli.conditions import have_text, hidden, visible

from integration.tests.fields import Button, Field, SearchableSelect, TextInput, enabled


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
        raise AssertionError(f'Page URL mismatch. Expected {instance.url},'
                             f'got {instance.browser.url}')
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


def requires_not_existing(locator, timeout=10):
    """Run method only after required element becomes visible"""

    @wrapt.decorator
    def _not_existing(wrapped, instance=None, args=None, kwargs=None):
        if not isinstance(instance, Page):
            raise ValueError('`not_existing` is only applicable to Page fields')
        instance.browser.element(locator).assure(lambda e: not e.exists, timeout)
        return wrapped(*args, **kwargs)

    return _not_existing


class LoginPage(Page):
    url = '/login'

    _username = TextInput(by_id('login-username-local'))
    _password = TextInput(by_id('login-password-local'))
    _sign_in = Button(by_css('button.bg-primary'))

    _modal_ok = Button(by_css('div.footer-actions .btn'))

    def login(self, next_url, username, password):
        """Login user and open URL

        :param str next_url: Target page url
        :param str username: Rancher user name
        :param str password: Rancher password
        """
        self.browser.open(next_url)
        self._username.input(username)
        self._password.input(password)
        self._sign_in.click()
        wait_for(self.browser, lambda b: b.url == next_url, timeout=10)

        # there can be optional information popup
        try:
            self._modal_ok.assure(visible, 1)
            self._modal_ok.click()
            self._modal_ok.assure(hidden)
        except TimeoutError:
            pass


class ClusterDriversListPage(Page):
    url = '/n/drivers/cluster'

    _add_driver = Button(by_xpath(r"//button[contains(., 'Add Cluster Driver')]"))

    @on_page
    def click_add_cluster_driver(self):
        self._add_driver.click()

    # register dialog

    _download_url = TextInput(by_xpath(r"//div[contains(., 'Download URL')]/input"))
    _custom_ui_url = TextInput(by_xpath(r"//div[contains(., 'Custom UI URL')]/input"))
    _add_domain = Button(by_xpath(r"//span[contains(., 'Add Domain')]"))
    _domain = TextInput(by_xpath(r"//span[@data-title='Whitelist Domains']/input"))
    _create = Button(by_xpath(r"//button[contains(., 'Create')]"))

    __modal_locator = by_css('form.modal-container.large-modal')

    @requires_visible(__modal_locator)
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

    @requires_not_existing(__modal_locator)
    def wait_for_activation(self):
        """Wait for driver to become 'Active'"""
        status_icon = self._otccce_line.sub_element('span')
        status_icon.should(have_text('Active'), 60)


class ClusterListPage(Page):
    url = '/g/clusters'

    _new_cluster_button = Button(r'.btn[href="/g/clusters/add"]')

    def click_new_cluster(self):
        self._new_cluster_button.click()


class NewClusterSelectPage(Page):
    url = '/g/clusters/add/select'

    _otc_cce_button = Button(r'div.machine-driver.otccce')

    def click_new_cce_cluster(self):
        self._otc_cce_button.click()


class CCEClusterConfigPage(Page):
    url = '/g/clusters/add/launch/otccce'

    # general
    _name = TextInput(r'input[id$="-form-name"]')

    def set_name(self, text):
        self._name.input(text)

    _save = Button(r'button[type=submit]')

    def next(self):
        self._save.should_be(enabled)
        self._save.click()

    _cancel = Button(by_xpath(r'//button[contains(., "Cancel")]'))

    _errors = Field(r'div.banner.bg-error')

    def cancel(self):
        self._cancel.click()

    # credentials
    _domain_name = TextInput(r'input.ember-text-field[name=domain-name]')
    _project_name = TextInput(r'input.ember-text-field[name=project-name]')
    _username = TextInput(r'input.ember-text-field[name=username]')
    _password = TextInput(r'input.ember-text-field[name=password]')

    def otc_login(self, domain, username, password, project):
        self._domain_name.input(domain)
        self._username.input(username)
        self._password.input(password)
        self._project_name.input(project)
        self.next()
        self._errors.should_be(hidden)

    # network configuration
    _vpc_selection = SearchableSelect(r'//div[./label[contains(text(), "Virtual Private Cloud")]]')

    def select_vpc(self, name):
        self._vpc_selection.select(name, 0)

    _subnet_selection = SearchableSelect(r'//div[./label[contains(text(), "Subnet")]]')

    def select_subnet(self, name):
        self._subnet_selection.select(name, 0)
