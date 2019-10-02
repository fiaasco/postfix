import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('postfix-centos')


def test_postfix_tls_main(host):
    """ basic configuration checks for TLS
    """
    f = host.file('/etc/postfix/main.cf')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('smtpd_use_tls = yes')
    assert f.contains('smtp_tls_security_level = may')
    assert f.contains('lmtp_tls_security_level = may')
    assert f.contains('smtpd_tls_cert_file = /etc/ssl/postfix-centos/postfix_postfix-centos.chain')
    assert f.contains('smtpd_tls_key_file = /etc/ssl/postfix-centos/postfix_postfix-centos.key')


@pytest.mark.parametrize('item', ['chain', 'key'])
def test_postfix_tls_chain(host, item):
    """ basic configuration checks for TLS
    """
    f = host.file('/etc/ssl/postfix-centos/postfix_postfix-centos.%s' % item)
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_postfix_tls(host):
    """ check whether postfix is offering TLS connections
    """
    command = host.run("openssl s_client -showcerts -connect localhost:25 -msg -ssl3")
    assert "CONNECTED" in command.stdout
    assert "SSL 3.0 Handshake" in command.stdout
    assert "Protocol  : SSLv3" in command.stdout
