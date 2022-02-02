import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    """ check if packages are installed
    """
    assert host.package('postfix').is_installed


def test_postfix_config(host):
    """ basic configuration checks
    """
    file = host.file('/etc/postfix/main.cf')
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644


def test_postfix_service(host):
    """ Testing whether the service is running and enabled
    """
    assert host.service('postfix').is_enabled
    assert host.service('postfix').is_running
