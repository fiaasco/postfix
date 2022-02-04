import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('postfix-ubuntu-bionic')


def test_postfix_tls_main(host):
    f = host.file('/etc/postfix/main.cf')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('smtpd_use_tls = yes')
    assert f.contains('smtp_tls_security_level = may')
    assert f.contains('lmtp_tls_security_level = may')
    assert f.contains('smtpd_tls_cert_file = /etc/ssl/postfix-ubuntu-bionic/postfix_postfix-ubuntu-bionic.chain')
    assert f.contains('smtpd_tls_key_file = /etc/ssl/postfix-ubuntu-bionic/postfix_postfix-ubuntu-bionic.key')


@pytest.mark.parametrize('item', ['chain', 'key'])
def test_postfix_tls_chain(host, item):
    """ basic configuration checks for TLS
    """
    f = host.file('/etc/ssl/postfix-ubuntu-bionic/postfix_postfix-ubuntu-bionic.%s' % item)
    assert f.exists
    assert f.user == 'postfix'
    assert f.group == 'postfix'


def test_postfix_tls(host):
    command = host.run("openssl s_client -showcerts -connect localhost:25 -msg -tls1_3")
    assert "CONNECTED" in command.stdout
    assert "TLS 1.3, Handshake" in command.stdout
    assert "SSL handshake has read" in command.stdout
