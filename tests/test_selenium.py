from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("http://127.0.0.1:8080")
assert "DellVE Dash: Portal Home" in driver.title
driver.find_element_by_class_name("page-scroll").click()
driver.find_element_by_tag_name("h2")
driver.find_element_by_css_selector("p.about-content")
driver.find_element_by_class_name("page-scroll-home").click()
driver.find_element_by_class_name("network-name").click()
assert driver.current_url == "https://github.com/dellve"
driver.execute_script("window.history.go(-1)")
elem = driver.find_element_by_name("server")
elem.clear()
elem.send_keys("10.157.26.8")
elem = driver.find_element_by_name("netdata_port")
elem.clear()
elem.send_keys("5555")
elem = driver.find_element_by_name("dellve_port")
elem.clear()
elem.send_keys("9999")
elem.send_keys(Keys.RETURN)
assert "DellVE Dash: System Metrics" in driver.title
driver.find_element_by_id("home-page")
driver.find_element_by_id("system-page")
driver.find_element_by_id("about-page")
driver.find_element_by_id("benchmark-page").click()
assert "DellVE Dash: Benchmarks" in driver.title
driver.find_element_by_class_name("form-group").click()
driver.find_element_by_id("benchmark-start-stop")
driver.find_element_by_id("home-page")
driver.find_element_by_id("system-page")
driver.find_element_by_id("benchmark-page")
driver.find_element_by_id("about-page").click()
assert "DellVE Dash: About" in driver.title
driver.find_element_by_class_name("network-name").click()
assert driver.current_url == "https://github.com/dellve"
driver.execute_script("window.history.go(-1)")
driver.find_element_by_id("about-page")
driver.find_element_by_id("system-page")
driver.find_element_by_id("benchmark-page")
driver.find_element_by_id("home-page").click()
assert "DellVE Dash: Portal Home" in driver.title
elem = driver.find_element_by_name("server")
elem.clear()
elem.send_keys("h")
elem = driver.find_element_by_name("netdata_port")
elem.clear()
elem.send_keys("p")
elem = driver.find_element_by_name("dellve_port")
elem.clear()
elem.send_keys("l")
elem.send_keys(Keys.RETURN)
assert "DellVE Dash: Invalid Server" in driver.title
driver.find_element_by_class_name("network-name").click()
assert driver.current_url == "https://github.com/dellve/dellve_dash"
driver.execute_script("window.history.go(-1)")
driver.find_element_by_class_name("home-page").click()
driver.close()
