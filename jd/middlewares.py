from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger





class SeleniumMiddleware():

    def __init__(self, timeout=None, service_args=[]):

        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome()
        #self.browser.set_window_size(1400, 700)
        #self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    

    def __del__(self):
        self.browser.close()

    

    def process_request(self, request, spider):

        """

        用CHROME抓取页面

        :param request: Request对象

        :param spider: Spider对象

        :return: HtmlResponse

        """

        self.logger.debug('PhantomJS is Starting')

        page = request.meta.get('page', 1)

        try:
            self.browser.get(request.url)
            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
                input.clear()
                input.send_keys(page)
                submit.click()
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_searchWrap .m-list')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)

        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    

    @classmethod
    def from_crawler(cls, crawler):

        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))

                   #service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))