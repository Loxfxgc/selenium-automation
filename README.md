# Selenium Test Automation for Web Application

This project contains automated test scripts using Selenium WebDriver to test the functionality of a sample e-commerce website (SauceDemo.com). The tests are written in Python using the unittest framework and cover key user workflows including login, shopping cart operations, and checkout process.

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver (automatically managed by webdriver-manager)

## Installation

1. Clone or download this repository to your local machine.

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - Selenium WebDriver
   - Webdriver Manager (for automatic ChromeDriver management)
   - Other supporting libraries

## Usage

### Running All Tests

To run all test cases with verbose output:
```bash
python app.py
```

### Running Specific Tests

You can run individual test methods using unittest's test discovery:
```bash
python -m unittest app.WebAppTestCase.test_01_login_success -v
```

Replace `test_01_login_success` with any of the available test methods.

## Test Cases

The automation suite includes the following test cases:

1. **test_01_login_success**: Verifies successful login with valid credentials
2. **test_02_login_failure**: Verifies login fails with invalid credentials and displays appropriate error message
3. **test_03_add_to_cart**: Tests adding items to the shopping cart and verifies cart badge updates
4. **test_04_remove_from_cart**: Tests removing items from the cart and verifies cart updates correctly
5. **test_05_checkout_process**: Tests the complete checkout workflow from adding items to order completion

## Configuration

The tests are configured to run in a visible Chrome browser window. For headless execution (running without opening a browser window), uncomment the following line in the `setUp` method of `app.py`:

```python
chrome_options.add_argument('--headless=new')
```

## Browser Setup

The tests use Chrome with the following configurations for stability:
- Disabled GPU acceleration
- Disabled sandbox mode
- Window size set to 1920x1080
- Automation detection disabled

## Error Handling

- Tests include proper exception handling and take screenshots on failures (saved as `test_XX_error.png`)
- Implicit waits and explicit waits are used for element synchronization
- Multiple click methods are attempted for reliability

## Dependencies

All required dependencies are listed in `requirements.txt`. Key packages include:
- `selenium==4.38.0`: WebDriver automation
- `webdriver-manager==4.0.2`: Automatic driver management
- Standard Python libraries for HTTP requests and utilities

## Notes

- The tests target the SauceDemo website (https://www.saucedemo.com/)
- Test data uses standard credentials: `standard_user` / `secret_sauce`
- Each test runs in a fresh browser instance for isolation
- Screenshots are automatically saved on test failures for debugging

## Troubleshooting

If you encounter issues:
1. Ensure Chrome browser is up to date
2. Check that all dependencies are installed correctly
3. Verify internet connection for accessing the test website
4. Check for any firewall/antivirus blocking ChromeDriver

For more information about Selenium WebDriver, visit the [official documentation](https://www.selenium.dev/documentation/).
# selenium-automation
