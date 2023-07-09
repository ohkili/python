

def Close_all_pop_up_return_main(driver):
    window_lst = driver.window_handles
    "main is main_lst[0], the other is pop up"
    for window in window_lst:
        if window != window_lst[0]:
            driver.switch_to.window(window)
            driver.close()
    driver.switch_to.window(window_lst[0])

    return driver

if __name__ == '__main__':
    pass