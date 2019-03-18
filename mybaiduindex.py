# !/usr/bin/python3.4
# -*- coding: utf-8 -*-


import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract

# 打开浏览器
def openbrowser():
    global browser
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"

    browser = webdriver.Firefox()
    browser.get(url)
    browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

    # 输入账号密码
    account = ['18826072046', 'nothing/']

    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

    # 点击登陆登陆
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆10秒
    print("等待网址加载完毕...")

    select = input("请观察浏览器网站是否已经登陆(y/n)：")
    while 1:
        if select == "y" or select == "Y":
            print("登陆成功！")
            print("准备打开新的窗口...")
            break

        elif select == "n" or select == "N":
            selectno = input("账号密码错误请按0，验证码出现请按1...")
            # 账号密码错误则重新输入
            if selectno == "0":
                browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
                browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

                # 输入账号密码
                account = ['18826072046', 'nothing/']
                browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
                browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

                # 点击登陆登陆
                browser.find_element_by_id("TANGRAM__PSP_3__submit").click()
            elif selectno == "1":
                input("请在浏览器中输入验证码并登陆...")
                select = input("请观察浏览器网站是否已经登陆(y/n)：")
        else:
            print("请输入“y”或者“n”！")
            select = input("请观察浏览器网站是否已经登陆(y/n)：")

def getindex(keyword, day):
    openbrowser()
    time.sleep(2)

    # 这里开始进入百度指数
    js = 'window.open("http://index.baidu.com");'
    browser.execute_script(js)
    # 获得当前打开所有窗口的句柄handles
    handles = browser.window_handles
    # 切换到当前最新打开的窗口
    browser.switch_to_window(handles[-1])
    # 清空输入框
    time.sleep(5)
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(keyword)
    # 点击搜索
    browser.find_element_by_id("searchWords").click()
    time.sleep(5)
    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)
    # 构造天数
    sel = '//a[@rel="' + str(day) + '"]'
    browser.find_element_by_xpath(sel).click()
    # 太快了
    time.sleep(2)

    if day == "all":
        day = 1000000

    # 储存数字的数组
    index = []
    try:
        # 截取当前浏览器
        path = "baidu/" + keyword
        browser.save_screenshot(str(path) + ".png")
        # 打开截图切割
        img = Image.open(str(path) + ".png")
        jpg = img.crop((600, 320, 700, 370))
        jpg.save(str(path) + "2.png")

        # 图像识别
        try:
            image = Image.open(str(path) + "2.png")
            code = pytesseract.image_to_string(image)
            if code:
                index.append（int(code.replace(",", "")))
            else:
                index.append("")
        except:
            index.append("")
    except Exception as err:
        print(err)

    print(index)
    file = open("baidu/index.txt", "w")
    for item in index:
        file.write(str(item) + "\n")
    file.close()



if __name__ == "__main__":
    # 每个字大约占横坐标12.5这样
    # 按照字节可自行更改切割横坐标的大小rangle
    keyword = input("请输入查询关键字：")
    sel = int(input("查询7天请按0，30天请按1，90天请按2，半年请按3，全部请按4："))
    day = 0
    if sel == 0:
        day = 7
    elif sel == 1:
        day = 30
    elif sel == 2:
        day = 90
    elif sel == 3:
        day = 180
    elif sel == 4:
        day = "all"
    getindex(keyword, day)
