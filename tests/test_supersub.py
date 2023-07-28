import pytest
from src.supersub import UnsupportedOSError, get_driver_path, get_chrome_path


def test_get_driver_path_mac(monkeypatch):
    monkeypatch.setattr('platform.system', lambda: 'Darwin')
    expected_path = './drivers/chromedriver_macos'
    result = get_driver_path()
    assert result == expected_path


def test_get_driver_path_linux(monkeypatch):
    monkeypatch.setattr('platform.system', lambda: 'Linux')
    expected_path = './drivers/chromedriver_linux'
    result = get_driver_path()
    assert result == expected_path


def test_get_driver_path_unsupported_os(monkeypatch):
    monkeypatch.setattr('platform.system', lambda: 'Windows')
    with pytest.raises(UnsupportedOSError):
        get_driver_path()


def test_get_chrome_path_mac(monkeypatch):
    monkeypatch.setenv('OS', 'Darwin')
    expected_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    result = get_chrome_path()
    assert result == expected_path


def test_get_chrome_path_linux(monkeypatch):
    monkeypatch.setenv('OS', 'Linux')
    expected_path = '/usr/bin/google-chrome-stable'
    result = get_chrome_path()
    assert result == expected_path


def test_get_chrome_path_unsupported_os(monkeypatch):
    monkeypatch.setenv('OS', 'Windows')
    with pytest.raises(UnsupportedOSError):
        get_chrome_path()
