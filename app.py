"""
Selenium Test Automation for Web Application
This script tests a sample e-commerce website (saucedemo.com)
Fixed version for better stability
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import unittest


class WebAppTestCase(unittest.TestCase):
    """Test cases for web application automation"""
    
    def setUp(self):
        """Setup that runs before each test - creates a new browser instance"""
        # Configure Chrome options for better stability
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Uncomment for headless mode
        # chrome_options.add_argument('--headless=new')
        
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(8)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Navigate to the application
        self.driver.get("https://www.saucedemo.com/")
        time.sleep(0.5)  # Brief pause for page stability
    
    def tearDown(self):
        """Cleanup that runs after each test"""
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"Error during teardown: {e}")
    
    def test_01_login_success(self):
        """Test Case 1: Verify successful login with valid credentials"""
        print("\n--- Running Test: Successful Login ---")
        
        try:
            # Locate and enter username
            username = self.wait.until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            username.clear()
            username.send_keys("standard_user")
            
            # Locate and enter password
            password = self.driver.find_element(By.ID, "password")
            password.clear()
            password.send_keys("secret_sauce")
            
            # Click login button
            login_btn = self.driver.find_element(By.ID, "login-button")
            login_btn.click()
            
            # Wait for products page to load
            products_title = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "title"))
            )
            
            # Verify successful login
            self.assertEqual(products_title.text, "Products")
            self.assertIn("inventory.html", self.driver.current_url)
            print("✓ Login successful - Products page loaded")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_02_login_failure(self):
        """Test Case 2: Verify login fails with invalid credentials"""
        print("\n--- Running Test: Failed Login ---")
        
        try:
            # Enter invalid credentials
            username = self.wait.until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            username.send_keys("invalid_user")
            
            password = self.driver.find_element(By.ID, "password")
            password.send_keys("wrong_password")
            
            # Click login button
            login_btn = self.driver.find_element(By.ID, "login-button")
            login_btn.click()
            
            # Wait for error message
            error_msg = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
            )
            
            # Verify error message is displayed
            self.assertIn("Username and password do not match", error_msg.text)
            print("✓ Error message displayed correctly")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_03_add_to_cart(self):
        """Test Case 3: Verify adding items to cart"""
        print("\n--- Running Test: Add to Cart ---")
        
        try:
            # Login first
            self._login()
            time.sleep(0.5)
            
            # Check if cart badge exists (should be empty initially)
            cart_badges = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
            initial_count = 0 if len(cart_badges) == 0 else int(cart_badges[0].text)
            
            # Add first item to cart
            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
            add_btn.click()
            
            time.sleep(0.5)  # Brief wait for cart to update
            
            # Verify cart badge appears and has correct count
            cart_badge = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
            )
            
            new_count = int(cart_badge.text)
            self.assertEqual(new_count, initial_count + 1)
            print(f"✓ Item added to cart successfully (Count: {new_count})")
            
        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_04_remove_from_cart(self):
        """Test Case 4: Verify removing items from cart"""
        print("\n--- Running Test: Remove from Cart ---")
        
        try:
            # Login and add item
            self._login()
            time.sleep(1)
            
            # Wait for page to be fully loaded
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
            )
            
            # Find add to cart button
            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
            
            # Try multiple click methods for reliability
            try:
                # Method 1: JavaScript click (most reliable)
                self.driver.execute_script("arguments[0].click();", add_btn)
            except:
                # Method 2: Regular click
                add_btn.click()
            
            # Wait for button to change to "Remove"
            time.sleep(1.5)
            
            # Verify the remove button exists (this proves item was added)
            remove_btn = self.wait.until(
                EC.presence_of_element_located((By.ID, "remove-sauce-labs-backpack"))
            )
            self.assertIsNotNone(remove_btn)
            print("✓ Item added to cart (Remove button appeared)")
            
            # Click remove button using JavaScript
            try:
                self.driver.execute_script("arguments[0].click();", remove_btn)
            except:
                remove_btn.click()
            
            time.sleep(1.5)
            
            # Verify the add button is back (this proves item was removed)
            add_btn_again = self.wait.until(
                EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
            self.assertIsNotNone(add_btn_again)
            
            # Also verify cart badge is gone
            cart_badges = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
            self.assertEqual(len(cart_badges), 0, "Cart should be empty after removing item")
            
            print("✓ Item removed from cart successfully")
            
        except Exception as e:
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot("test_04_error.png")
                print("Screenshot saved as test_04_error.png")
            except:
                pass
            self.fail(f"Test failed with error: {str(e)}")
    
    def test_05_checkout_process(self):
        """Test Case 5: Verify complete checkout process"""
        print("\n--- Running Test: Checkout Process ---")
        
        try:
            # Login and add item
            self._login()
            time.sleep(1)
            
            add_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
            add_btn.click()
            time.sleep(1)
            
            # Go to cart
            cart_link = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
            )
            cart_link.click()
            time.sleep(1)

            # Wait for the cart page to actually load by checking for its title or unique element
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
            )

            # Proceed to checkout
            checkout_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "checkout"))
            )
            checkout_btn.click()
            time.sleep(1)
            
            # Fill checkout information
            first_name = self.wait.until(
                EC.presence_of_element_located((By.ID, "first-name"))
            )
            first_name.send_keys("John")
            
            last_name = self.driver.find_element(By.ID, "last-name")
            last_name.send_keys("Doe")
            
            postal_code = self.driver.find_element(By.ID, "postal-code")
            postal_code.send_keys("12345")
            
            time.sleep(0.5)
            
            # Continue
            continue_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "continue"))
            )
            continue_btn.click()
            time.sleep(1)
            
            # Finish checkout
            finish_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "finish"))
            )
            finish_btn.click()
            time.sleep(1)
            
            # Verify order completion
            complete_header = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
            )
            
            self.assertEqual(complete_header.text, "Thank you for your order!")
            print("✓ Checkout completed successfully")
            
        except Exception as e:
            try:
                self.driver.save_screenshot("test_05_error.png")
                print("Screenshot saved as test_05_error.png")
            except:
                pass
            self.fail(f"Test failed with error: {str(e)}")
    
    def _login(self):
        """Helper method to perform login"""
        username = self.wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username.send_keys("standard_user")
        
        password = self.driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        
        login_btn = self.driver.find_element(By.ID, "login-button")
        login_btn.click()
        
        # Wait for products page
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )


if __name__ == "__main__":
    # Run the tests with verbose output
    unittest.main(verbosity=2)