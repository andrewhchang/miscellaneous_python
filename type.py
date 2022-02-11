import asyncio
import pyppeteer as pup
import time

url = 'https://play.typeracer.com'
interval = 0.03
suffix = 'change display format'

async def main():
    try:
        browser = await pup.launch({
            'headless': False,
            'defaultViewport': None,
            'args': ['--incognito']
        })

        pages = await browser.pages()
        page = pages[0]

        await page.goto(url)

        while True:
                print('ready to begin race?')
                await find_and_race(page)
    except Exception as e:
        None

async def find_and_race(page):
    print('press any key when there is text on the page')
    input()

    print('grabbing input...')
    content = await page.querySelector('.inputPanel')
    textbox_content = await page.evaluate('(element) => element.textContent', content)
    text = textbox_content[:-len(suffix)]

    print("press any key when ready to type")
    input()

    inp = await page.querySelector('.txtInput')
    await inp.focus()
    print("racing...")

    for char in text:
        time.sleep(interval)
        await page.keyboard.type(char)
    print("race completed")

asyncio.get_event_loop().run_until_complete(main())
