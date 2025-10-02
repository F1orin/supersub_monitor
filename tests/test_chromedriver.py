"""
Test ChromeDriver manager functionality with mocking for CI compatibility.
"""

from unittest.mock import MagicMock, patch
import pytest


class TestChromeDriverManager:
    """Test ChromeDriver manager functionality."""
    
    @patch('chromedriver_manager.webdriver.Chrome')
    @patch('chromedriver_manager.ChromeDriverManager')
    def test_create_driver_function(self, mock_chrome_manager, mock_chrome_class):
        """Test driver creation function."""
        # Setup mocks
        mock_service = MagicMock()
        mock_chrome_manager.return_value.install.return_value = '/mock/path/chromedriver'
        
        mock_driver = MagicMock()
        mock_chrome_class.return_value = mock_driver
        
        # Test driver creation
        from chromedriver_manager import create_driver
        driver = create_driver()
        
        # Verify Chrome was called with correct arguments
        mock_chrome_manager.return_value.install.assert_called_once()
        mock_chrome_class.assert_called_once()
        
        # Verify the driver instance
        assert driver == mock_driver
    
    @patch('chromedriver_manager.create_driver')
    def test_get_driver_singleton(self, mock_create_driver):
        """Test get_driver returns singleton instance."""
        mock_driver = MagicMock()
        mock_create_driver.return_value = mock_driver
        
        from chromedriver_manager import get_driver, shutdown_driver
        
        # Clear any existing driver
        shutdown_driver()
        
        # First call should create driver
        driver1 = get_driver()
        mock_create_driver.assert_called_once()
        
        # Second call should return same driver (mock the internal _driver)
        driver2 = get_driver()
        assert driver1 == driver2
    
    def test_shutdown_driver_functionality(self):
        """Test driver shutdown functionality."""
        from chromedriver_manager import shutdown_driver
        
        # Should not crash even if no driver exists
        shutdown_driver()  # This should succeed
    
    @patch('chromedriver_manager.webdriver.Chrome')
    def test_driver_options(self, mock_chrome_class):
        """Test that correct Chrome options are set."""
        with patch('chromedriver_manager.ChromeDriverManager') as mock_manager:
            mock_manager.return_value.install.return_value = '/mock/path/chromedriver'
            
            from chromedriver_manager import create_driver
            create_driver()
            
            # Verify Chrome was created with service
            mock_chrome_class.assert_called_once()
            call_args = mock_chrome_class.call_args
            
            # Should have service argument
            assert 'service' in call_args.kwargs
            assert 'options' in call_args.kwargs
