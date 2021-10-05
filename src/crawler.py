import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

URL = "https://en.wikipedia.org/wiki/Main_Page"
FIREFOX_DRIVER_PATH = "./Driver/geckodriver"
NULL_PATH = "/dev/null"
MAX_DEPTH = 5
MAX_CHILDREN = 2


class Crawler:
    def __init__(self, link=None, depth=0) -> None:
        self.link = link
        self.depth = depth
        self.children = []

        self.title = None
        self.driver = None
        self.has_children = False
        self.max_depth = MAX_DEPTH

        self.set_driver()

    def set_driver(self) -> None:
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options,
                                        executable_path=FIREFOX_DRIVER_PATH,
                                        service_log_path=NULL_PATH)

    def set_start(self) -> None:
        self.driver.get(URL)
        time.sleep(3)
        self.driver.find_element_by_xpath('//a[@href="'+"/wiki/Special:Random"+'"]').click()
        self.link = str(self.driver.current_url)

    def burrow(self) -> None:
        if self.depth < self.max_depth:
            if not self.has_children:
                self.dig()
            for child in self.children:
                if child:
                    child.burrow()

    def dig(self) -> None:
        '''
            "self.max_depth = self.depth" stops this crawler from burrowing any deeper, as this assures
            the condition on line 41 will fail.
        '''
        if not self.link:
            print('Failed at line 53')
            self.max_depth = self.depth
            return
        else:
            self.driver.get(self.link)
            time.sleep(3)

            try:
                self.title = (self.driver.find_element_by_id("firstHeading")).text
            except:
                print('Failed at line 63')
                self.max_depth = self.depth
                self.driver.quit()
                return

            # Select a random paragraph from the article
            paragraphs = self.driver.find_elements_by_tag_name('p')
            paragraphs = [p for p in paragraphs if p.text != ''] # Remove empty paragraphs
            if len(paragraphs) == 0:
                print('Failed at line 72')
                self.max_depth = self.depth
                self.driver.quit()
                return

            par = paragraphs[random.randint(0, len(paragraphs)-1)]
            links = par.find_elements_by_tag_name('a') # Gather all the links in the chosen paragraph

            # Make a list of MAX_CHILDREN many indices for which we will use to select our links
            options = [i for i in range(len(links))]
            indices = []

            i = 0
            while i < MAX_CHILDREN and len(options) > 0:
                choice = random.randint(0, len(options)-1)
                indices.append(options[choice])
                del options[choice] # This makes sure we cannot select the same index twice
                i += 1

            # Finally, create children based off of selected links
            for i in range(len(indices)):
                link = str(links[indices[i]].get_attribute("href"))
                self.children.append(Crawler(link, self.depth+1))
            self.has_children = True

            self.driver.quit()

    def show(self) -> None:
        if self.title:
            print((' ' * 4) * self.depth, self.depth, self.title)
        if self.has_children:
            for child in self.children:
                child.show()


