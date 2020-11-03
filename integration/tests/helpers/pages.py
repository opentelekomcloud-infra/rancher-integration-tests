import wrapt
from pyasli import wait_for
from pyasli.bys import by_css, by_id, by_xpath
from pyasli.conditions import enabled, hidden, visible

from integration.tests.helpers.base import Field, Page, on_page
from integration.tests.helpers.fields import (
    Button, ClusterDriverRow, ClusterRow, SearchSelect, TextInput
)


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

        # there can be optional information popup
        self._close_optional_modal()

    def __modal_shown(self):
        try:
            wait_for(self._modal_ok, visible, 1)
            return True
        except TimeoutError:
            return False

    def _close_optional_modal(self):
        if not self.__modal_shown():
            return
        self._modal_ok.click()
        self._modal_ok.assure(hidden)


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
    @property
    def driver_row(self):
        row = ClusterDriverRow('kontainer-engine-driver-otccce')
        row.__refresh__(self.browser)
        return row


class ClusterListPage(Page):
    url = '/g/clusters'

    _new_cluster_button = Button(r'.btn[href="/g/clusters/add"]')

    def click_new_cluster(self):
        self._new_cluster_button.click()

    def cluster_row(self, name):
        row = ClusterRow(name)
        # refresh row, as it's not processed in usual workflow
        row.__refresh__(self.browser)
        return row


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
    _password = TextInput(r'input.ember-text-field[name=passsword]')

    def input_credentials(self, domain, username, password, project):
        self._domain_name.input(domain)
        self._username.input(username)
        self._password.input(password)
        self._project_name.input(project)

    # network configuration
    _vpcs = SearchSelect(r'//div[./label[contains(text(), "Virtual Private Cloud")]]')

    def select_vpc(self, name):
        self._vpcs.select(name, 0)

    _subnet_selection = SearchSelect(r'//div[./label[contains(text(), "Subnet")]]')

    def select_subnet(self, name):
        self._subnet_selection.select(name)

    # node configuration
    _ssh_keys = SearchSelect(r'//div[./label[contains(text(), "SSH Key Pair")]]')

    def select_key_pair(self, name):
        self._ssh_keys.select(name)


class ClusterDashboardPage(Page):
    _more_actions = Button('div.more-actions')
    _delete_button = Button(r'//span[contains(text(), "Delete")]')
    _delete_confirm_button = Button('div.footer-actions .bg-error')

    def delete(self):
        self._more_actions.click()
        self._delete_button.click()
        self._delete_confirm_button.click()
