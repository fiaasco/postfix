import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('postfix-debian-10')


def test_postfix_tls_main(host):
    """ basic relay configuration check
    """
    f = host.file('/etc/postfix/main.cf')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('relayhost = relay.mol.ecule')
