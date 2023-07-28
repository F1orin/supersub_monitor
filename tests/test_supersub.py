import pytest
from src.supersub import UnsupportedOSError, get_driver_path


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
