# Supersub Monitor Tests

Basic tests to verify the project runs correctly and dependencies work fine.

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_imports.py

# Run with shorter traceback
python -m pytest tests/ --tb=short
```

## Test Structure

- `test_imports.py` - Verify all dependencies can be imported
- `test_config.py` - Test environment loading and logging setup
- `test_chromedriver.py` - Test ChromeDriver manager (mocked for CI)
- `test_main.py` - Test main entry point with mocked dependencies
- `conftest.py` - Pytest fixtures and configuration

## Test Features

- **No external dependencies** - All WebDriver operations are mocked
- **Environment isolation** - Tests don't interfere with real `.env` files
- **CI-friendly** - Works without Chrome/Selenium installation
- **Comprehensive coverage** - Tests imports, config, lifecycle, and error cases

## What the Tests Verify

✅ All required packages can be imported  
✅ Environment variables are loaded correctly  
✅ ChromeDriver manager functions work (mocked)  
✅ Main application entry point runs  
✅ Command line arguments are parsed correctly  
✅ Missing environment variables are handled gracefully
