from playwright.sync_api import sync_playwright
from datetime import datetime

with sync_playwright() as playwright:
    start_time = datetime.now()

    # Launch a browser
    browser = playwright.chromium.launch(headless=False) # headless=False : ให้หน้า browser ขึ้นมาเวลารันเป็นเวลา slow_mo=500 : pop-up ขึ้นมาเป็นเวลา 0.5 secs
    # Create a new page
    page = browser.new_page()

    target_url = 'https://userdb.diw.go.th/factoryPublic/tumbol.asp'

    page.goto(target_url)

    area_arr = []

    area = page.locator('//a').all()

    for a in area:
        area_arr.append(a.text_content())

    # Loop area
    for a in area_arr:
        page.locator(f"//a[text()='{a}']").click()

        province_arr = []

        province = page.locator("//a[contains(text(),'จ.')]").all()

        for p in province:
            province_arr.append(p.text_content())

        # Loop province
        for p in province_arr:
            page.locator(f"//a[text()='{p}']").click()

            district_arr = []

            district = page.locator("//a[contains(text(),'อ.')]").all()

            for d in district:
                district_arr.append(d.text_content())

            # Loop district
            for d in district_arr:
                page.locator(f"//a[text()='{d}']").click()

                # Start waiting for the download
                with page.expect_download() as download_info:
                    # Perform the action that initiates download
                    page.locator(f"//a[contains(text(),'download')]").click()

                download = download_info.value

                file_output_path = f"./diw/{a}/{download.suggested_filename}"

                # Wait for the download process to complete and save the downloaded file somewhere
                download.save_as(file_output_path)
                page.reload()

    browser.close() 

    end_time = datetime.now()
    diff_time = end_time - start_time
    print(diff_time)
