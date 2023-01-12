import time

def test_search_example(selenium):
    """Search some text in google and make screenshot"""
    selenium.get("https://google.com")
    time.sleep(5)

    # find element and input text
    search_input = selenium.find_element('name', 'q')
    search_input.clear()
    search_input.send_keys('first test')
    time.sleep(10)
    # find button and click to find

    element = selenium.find_element('name', 'btnK')
    element.click()

    time.sleep(5)
    selenium.save_screenshot('result.png')

