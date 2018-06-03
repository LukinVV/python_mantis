import pytest
import json
import os.path
import jsonpickle
import ftputil
from fixture.application import Application
from fixture.orm import ORMFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture()
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    # web_config = load_config(request.config.getoption("--target"))['web']
    # web_admin_config = load_config(request.config.getoption("--target"))['webadmin']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser,  config = config) #base_url=config["web"]["baseUrl"])
    fixture.session.ensure_login(username=config['webadmin']['user_name'], password=config['webadmin']['password'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())


@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")


@pytest.fixture(scope="session")
def orm(request, config):
    ormfixture = ORMFixture(host=config['db']['host'], name=config['db']['name'], user=config['db']['user'],
                          password=config['db']['password'])
    return ormfixture


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configurtion(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php","config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__),"resources/config_inc.php"), "config_inc.php")


def restore_server_configurtion(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak","config_inc.php")