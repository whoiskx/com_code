from setting import driver_facebook, execute_times, log

try:
    driver = driver_facebook()
    driver.get('https://www.facebook.com/profile.php?id=100018160331338')
    execute_times(driver, 1200)
    html = driver.page_source
    with open('index_xihaiming.html', 'w', encoding='utf-8') as f:
        f.write(html)
except Exception as e:
    log('error', e)
