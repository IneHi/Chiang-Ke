"""
Half Auto CourseSelection
Written by Inehi
Special thank to Jeff
"""
import asyncio
from pyppeteer import launch
import fuckcaptcha as fucking
import time
import pyppeteer
import requests
############################################
# Custom INFO
username = "B11002215"
password = "08.NTUST.ece"
course = ["BAG006301"]
url = "https://courseselection.ntust.edu.tw/AddAndSub/B01/B01"
Line_Notify_token = "bdXJzcqSWjMYoN28mAtR5xd55Td1KJBEkrumNr8GFyc"
headers = {"Authorization" : "Bearer " + Line_Notify_token, "Content-Type": "application/x-www-form-urlencoded"}
i = 0
############################################
async def main():

    async def login():
        try:
            await page.goto('https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection')
            await page.type("[name='UserName']", username)
            await page.type("[name='Password']", password + '\n')
            await page.waitForNavigation()
        except pyppeteer.errors.TimeoutError:
            print("Login Fail")
            return 0

   

    browser = await launch(autoClose=False, headless=False, dumpio=True,
                           args=['--disable-infobars', '--window-size=782,831'])
    page = await browser.newPage()
    await page.setViewport({'width': 782, 'height': 831})
    # Makes me don't look like a WebDriver
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => false } }) }')
    await fucking.bypass_detections(page)

    async def close_dialog(dialog):
        print(dialog.message)
        await dialog.dismiss()
        if dialog.message == "這門課已經在您的選課表或已經修過，請勿重複選課(課碼、課名重複)。":
            requests.post("https://notify-api.line.me/api/notify", headers=headers, data={"message": "搶到" + i + "了"})
            course.remove(i)
            if not course:
                await browser.close()
        


    page.on( # start listening to js alert
        'dialog',
        lambda dialog: asyncio.ensure_future(close_dialog(dialog))
    )
    await login()
    await page.goto(url)
    while True:
        try:
            for i in course:
                await page.waitForSelector("[name='CourseText']", {'timeout': 1000})
                await page.type("[name='CourseText']", i)
                await page.click("[id='SingleAdd']")
                await page.waitForNavigation()
        except pyppeteer.errors.TimeoutError:
            print("No item to select")
            if page.url == "https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection":
                print("Re login")
                await fucking.bypass_detections(page)
                await login()
            elif page.url == "https://courseselection.ntust.edu.tw/Home/Error?message=%E4%B8%8D%E5%85%B7%E6%AD%A4%E7%B3%BB%E7%B5%B1%E4%BD%BF%E7%94%A8%E4%B9%8B%E6%AC%8A%E9%99%90%2CYou%20can%27t%20use%20this%20System":
                print("Re login")
                await fucking.bypass_detections(page)
                await login()
            elif page.url != url:
                print("Re direct")
                await page.goto(url)






asyncio.get_event_loop().run_until_complete(main())