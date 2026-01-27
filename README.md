# Selenium Python Automation Framework

A scalable, maintainable Selenium automation framework using Python 3.12, PyTest, and the Page Object Model (POM) design pattern. This framework is built following industry best practices for web automation testing with mobile emulation support.

## Features

✅ **Page Object Model (POM)**: Clean separation of test logic and page elements
✅ **Explicit Waits**: No `time.sleep()` or implicit waits - uses WebDriverWait throughout
✅ **Mobile Emulation**: Chrome mobile device emulation (iPhone 12 Pro default)
✅ **PyTest Framework**: Modern testing framework with fixtures and plugins
✅ **Headless Mode**: Configurable headless execution for CI/CD
✅ **Screenshot on Failure**: Automatic screenshot capture when tests fail
✅ **Modal Handling**: Built-in support for popups and modals
✅ **GitHub Actions**: Pre-configured CI/CD pipeline
✅ **HTML Reports**: Beautiful test execution reports with pytest-html

## Project Structure

```
seltask/
├── .github/workflows/
│   └── test.yml                 # GitHub Actions CI/CD configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # PyTest fixtures & hooks
│   └── test_twitch.py           # Twitch test cases
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base page with common methods
│   ├── twitch_home_page.py      # Twitch home page object
│   ├── twitch_search_page.py    # Twitch search page object
│   └── twitch_stream_page.py    # Twitch stream page object
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration settings
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py        # WebDriver factory
│   └── helpers.py               # Helper functions
├── reports/                      # Test execution reports
├── screenshots/                  # Screenshots on test failure
├── requirements.txt              # Python dependencies
├── pytest.ini                    # PyTest configuration
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12+
- Google Chrome browser
- Git

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd seltask
```

2. **Create and activate virtual environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

The framework will automatically download and manage ChromeDriver using Selenium Manager (built into Selenium 4.6+).

## Configuration

Main configuration is in `config/settings.py`:

- **BASE_URL**: Target website URL (default: https://www.twitch.tv)
- **EXPLICIT_WAIT_TIMEOUT**: Default timeout for explicit waits (10 seconds)
- **PAGE_LOAD_TIMEOUT**: Maximum page load time (30 seconds)
- **DEFAULT_DEVICE**: Mobile device to emulate (iPhone 12 Pro)
- **HEADLESS_MODE**: Run browser in headless mode (default: False)

## Usage

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run in headless mode:**
```bash
pytest --headless
```

**Run with custom mobile device:**
```bash
pytest --device-name="Pixel 5"
```

**Run specific test:**
```bash
pytest tests/test_twitch.py::test_twitch_starcraft_stream -v
```

**Run with test markers:**
```bash
# Run only smoke tests
pytest -m smoke

# Run Twitch-specific tests
pytest -m twitch
```

**Generate HTML report:**
```bash
pytest --html=reports/report.html --self-contained-html
```

### Available Command-Line Options

- `--headless`: Run browser in headless mode
- `--device-name=DEVICE`: Specify mobile device (iPhone 12 Pro, Pixel 5, Custom)
- `--html=PATH`: Generate HTML report at specified path
- `-v`: Verbose output
- `-s`: Show print statements
- `-k EXPRESSION`: Run tests matching expression

## Test Cases

### Main Test: StarCraft II Stream Search

**Test:** `test_twitch_starcraft_stream`

**Steps:**
1. Navigate to twitch.com
2. Click the search icon
3. Input "StarCraft II" in search
4. Scroll down 2 times
5. Select a streamer (first available)
6. Handle any modals/popups (mature content, consent banners)
7. Verify stream loaded successfully

**Usage:**
```bash
pytest tests/test_twitch.py::test_twitch_starcraft_stream -v -s
```

### Additional Tests

- `test_twitch_homepage_loads`: Smoke test for homepage loading
- `test_twitch_search_opens`: Verify search functionality is accessible

## Framework Architecture

### Page Object Model

Each page is represented by a class that inherits from `BasePage`:

```python
from pages.twitch_home_page import TwitchHomePage

home_page = TwitchHomePage(driver)
home_page.open()
home_page.click_search_icon()
```

### Base Page Methods

Common methods available in all page objects:

- `find_element(locator)`: Find element with explicit wait
- `find_elements(locator)`: Find multiple elements
- `click(locator)`: Click element with wait for clickability
- `type(locator, text)`: Type text into input field
- `wait_for_element_visible(locator)`: Wait for element visibility
- `wait_for_element_clickable(locator)`: Wait for element clickability
- `wait_for_invisibility(locator)`: Wait for element to disappear
- `scroll_down(times)`: Scroll page down
- `take_screenshot(name)`: Capture screenshot
- `handle_modal_if_present(modal_locator, close_button)`: Handle popups

### WebDriver Factory

Centralized WebDriver creation with mobile emulation:

```python
from utils.driver_factory import DriverFactory

# Create driver with default settings
driver = DriverFactory.create_driver()

# Create driver with custom settings
driver = DriverFactory.create_driver(headless=True, device_name="Pixel 5")
```

## Best Practices Implemented

1. **Explicit Waits Only**: All waits use `WebDriverWait` with `ExpectedConditions` - NO `time.sleep()` or implicit waits
2. **Session-Scoped Fixtures**: WebDriver reused across tests for efficiency
3. **Screenshot on Failure**: Automatic debugging aid
4. **Multiple Locator Strategies**: Fallback locators for reliability
5. **Mobile Emulation**: Tests run in mobile viewport as required
6. **Configurable Execution**: Headless mode and device selection
7. **Clean Code**: PEP 8 compliant, well-documented
8. **Proper Synchronization**: URL change detection and element state verification

## CI/CD with GitHub Actions

The framework includes a GitHub Actions workflow (`.github/workflows/test.yml`) that:

1. Runs on push to `main` or `develop` branches
2. Runs on pull requests
3. Sets up Python 3.12
4. Installs Chrome browser
5. Installs dependencies
6. Executes tests in headless mode
7. Uploads test reports as artifacts
8. Uploads screenshots on failure

**To enable GitHub Actions:**
1. Push your code to GitHub
2. The workflow will run automatically
3. Check the "Actions" tab for results
4. Download artifacts for reports and screenshots

## Troubleshooting

### ChromeDriver Issues

The framework uses Selenium Manager (built into Selenium 4.6+) to automatically download and manage ChromeDriver. If you encounter issues:

```bash
# Clear Selenium cache
rm -rf ~/.cache/selenium

# Reinstall selenium
pip uninstall selenium
pip install selenium==4.18.0
```

### Element Not Found Errors

- Check if locators need updating (Twitch UI may change)
- Increase `EXPLICIT_WAIT_TIMEOUT` in `config/settings.py`
- Check screenshots in `screenshots/` directory for debugging

### Tests Fail in Headless Mode

Some elements may behave differently in headless mode:
- Try running without `--headless` first
- Check viewport size in `driver_factory.py`
- Ensure mobile emulation is working correctly

### Modal Handling Issues

If mature content or other modals aren't handled:
- Update locators in `twitch_stream_page.py`
- Increase timeout in `handle_modals()` method
- Check screenshot for actual modal structure

## Extending the Framework

### Adding New Page Objects

1. Create new file in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class attributes
4. Implement page-specific methods

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class NewPage(BasePage):
    # Locators
    ELEMENT = (By.ID, "element-id")

    def perform_action(self):
        self.click(self.ELEMENT)
```

### Adding New Tests

1. Create test file in `tests/` directory (must start with `test_`)
2. Import required page objects
3. Use `driver` fixture
4. Add test markers if needed

```python
import pytest
from pages.new_page import NewPage

@pytest.mark.smoke
def test_new_feature(driver):
    page = NewPage(driver)
    page.perform_action()
    assert page.is_element_visible(page.ELEMENT)
```

### Adding New Mobile Devices

Update `MOBILE_DEVICES` in `config/settings.py`:

```python
MOBILE_DEVICES = {
    "Custom Device": {
        "deviceMetrics": {
            "width": 414,
            "height": 896,
            "pixelRatio": 2.0
        },
        "userAgent": "Mozilla/5.0..."
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Future Enhancements

- [ ] Selenium Grid integration for parallel execution
- [ ] Cross-browser support (Firefox, Safari, Edge)
- [ ] Data-driven testing with PyTest parametrize
- [ ] API testing integration
- [ ] Allure reporting
- [ ] Docker containerization
- [ ] Visual regression testing
- [ ] Performance metrics collection

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue in the repository.

---

**Happy Testing!** 🎉🧪
