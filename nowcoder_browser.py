import configparser
import os.path
from http.cookies import SimpleCookie

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_cookie_dict(s: str) -> dict:
    """
        字符串饼干转字典
    """
    tmp = SimpleCookie()
    tmp.load(s)
    return {k: v.value for k, v in tmp.items()}


class Nowcoder_browser:
    BASE_PATH = "https://ac.nowcoder.com/acm/contest/"
    CLASS_NAME = "question-module"

    def __init__(self, contest_id, min_problem: str, max_problem: str, w, h, out_path, chromedrive_path, cookie_string):
        self.contest_id = contest_id
        self.min_problem = min_problem
        self.max_problem = max_problem
        self.w = int(w)
        self.h = int(h)
        self.out_path = out_path
        self.chromedrive_path = chromedrive_path
        self.cookie_string = cookie_string

        self.url = self.BASE_PATH + self.contest_id

    def run(self):
        # 使用移动设备截图
        chrome_opt = Options()
        mobile_emulation = {
            "deviceMetrics": {
                "width": self.w,
                "height": self.h
            }
        }
        chrome_opt.add_experimental_option("mobileEmulation", mobile_emulation)
        d = webdriver.Chrome(chrome_options=chrome_opt, executable_path=self.chromedrive_path)
        d.get(self.url)

        # cookie
        cookie_dict = get_cookie_dict(self.cookie_string)
        for k, v in cookie_dict.items():
            d.add_cookie({'name': k, 'value': v})

        # 截图
        if not os.path.exists(self.out_path):
            os.mkdir(self.out_path)
        for x in range(ord(self.min_problem), ord(self.max_problem) + 1):
            c = chr(x)

            d.get(self.url + '/' + c)
            ele = d.find_element_by_class_name(self.CLASS_NAME)
            if ele:
                print("Yes: Get problem " + c)
                ele.screenshot(os.path.join(self.out_path, f'Problem_{c}.png'))


def work():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    config_dict = config['DEFAULT']

    Cookie_string = ""
    with open("Cookie.txt", "r") as f:
        for line in f:
            Cookie_string += line

    nc = Nowcoder_browser(
        config_dict['Contest_id'],
        config_dict['Min_problem_char'],
        config_dict['Max_problem_char'],
        config_dict['Width'],
        config_dict['Height'],
        config_dict['Out_path'],
        config_dict['Chromedrive_path'],
        Cookie_string
    )

    nc.run()


if __name__ == '__main__':
    work()
