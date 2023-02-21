import asyncio
from pyppeteer import launch  # 控制模拟浏览器用
from pyppeteer.dialog import Dialog

js1 = '''() =>{Object.defineProperties(navigator,{webdriver:{get: () => undefined} })}'''
js2 = '''() => {alert ( window.navigator.webdriver )}'''


async def main(url):  # 定义main协程函数，
    # 插件路径
    args = ['--no-sandbox',
            '--disable-gpu',
            '--log-level=3',  # 日志等级
            '--disable-infobars',  # 关闭提示
            '--window-size={},{}'.format(1080, 950),
            ]


    # dumpio:True 浏览器就不会卡住了
    # 浏览器启动参数
    params = {"userDataDir": r"D:\temporary",
              'headless': False,
              'args': args,
              'dumpio': True}
    browser = await launch(params)  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36')

    # 设置页面超时
    page.setDefaultNavigationTimeout(1000 * 60)  # 60s
    # 启用js
    await page.setJavaScriptEnabled(True)
    # 启用拦截器
    # await page.setRequestInterception(True)
    await page.evaluate(js1)
    await page.evaluate(js2)
    await page.setViewport({'width': 1300, 'height': 868})  # 设置界面
    page.on('dialog', lambda dialog: asyncio.ensure_future(handle_dialog(page, dialog)))
    await page.goto(url)  # 访问登录页面
    await asyncio.sleep(5)
    await browser.close()


async def handle_dialog(page, dialog: Dialog):
    print(dialog.message)  # 打印出弹框的信息
    print(dialog.type)  # 打印出弹框的类型，是alert、confirm、prompt哪种
    # print(dialog.defaultValue())#打印出默认的值只有prompt弹框才有
    await page.waitFor(2000)  # 特意加两秒等可以看到弹框出现后取消
    await dialog.dismiss()


# await dialog.accept(‘000’) #可以给弹窗设置默认值


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    loop = asyncio.get_event_loop()
    m = main(url)
    loop.run_until_complete(m)