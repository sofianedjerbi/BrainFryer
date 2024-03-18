import logging
import re
from playwright.sync_api import sync_playwright

BLACKLIST = [
    "cock", "dick", "prostitute", "slut", "bitch", "nigga", "retarded", "nigger",
    "fuck", "cunt", "whore", "faggot", "tranny", "shemale", "pussy", "bastard", 
    "bollocks", "cum", "fag", "queer", "sissy", "twat", "wank", "arsehole", "porn",
    "asshole", "bellend", "pube", "shit", "spunk", "tit", "tosser", "turd", "vagina", "wanker",
    "kraut", "polack", "sambo", "slopey", "tacohead", "wetback", "zipperhead"
]

logger = logging.getLogger(__name__)

blacklist_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BLACKLIST)) + r')\b', re.IGNORECASE)

class RedditAgent:
    def __init__(self, image_path):
        self.image_path = image_path
    
    def parse_reddit_post(self, url, maximum=10):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-position=0,0',
                '--ignore-certifcate-errors',
                '--ignore-certifcate-errors-spki-list',
                '--disable-extensions',
                '--disable-dev-shm-usage',
                '--start-maximized'
            ])

            context = browser.new_context(
                device_scale_factor=2,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
            )

            page = context.new_page()
            page.goto(url)

            for i in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(500)
                if page.is_visible('text="View more comments"'):
                    page.click('text="View more comments"')
                page.wait_for_timeout(1000)

            title_element = page.query_selector("h1")
            title_text = title_element.text_content().strip()
            logger.debug(f"Title: {title_text}")

            title_element = page.query_selector("//shreddit-post")
            title_element.screenshot(path=f"{self.image_path}/reddit_0.png")
            
            comments = page.query_selector_all("//shreddit-comment[@depth='0']")

            comments_list = []
            nb = 1
            for comment in comments:
                if nb > maximum:
                    continue
                author_div = comment.query_selector('[slot="commentMeta"]')
                message_div = comment.query_selector('[slot="comment"]')

                if message_div is None or author_div is None:
                    continue

                comment_text = message_div.text_content()
                cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', comment_text)
                cleaned_text = re.sub(r'[\r\t]', ' ', cleaned_text)
                cleaned_text = re.sub(r' +', ' ', cleaned_text)
                cleaned_text = re.sub(r'\n +| +\n', '\n', cleaned_text)
                cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
                cleaned_text = cleaned_text.strip().strip("\n").strip("\t").strip("\r")

                if len(cleaned_text) > 220:
                    continue

                if bool(blacklist_pattern.search(cleaned_text)):
                    continue

                logger.debug(f"Adding comment: {cleaned_text}")
                comments_list.append(cleaned_text)

                author_div.scroll_into_view_if_needed()
                message_div.scroll_into_view_if_needed()

                author_bounding_box = author_div.bounding_box()
                message_bounding_box = message_div.bounding_box()

                combined_top = min(author_bounding_box['y'], message_bounding_box['y'])
                combined_left = min(author_bounding_box['x'], message_bounding_box['x'])
                combined_right = max(author_bounding_box['x'] + author_bounding_box['width'], message_bounding_box['x'] + message_bounding_box['width'])
                combined_bottom = max(author_bounding_box['y'] + author_bounding_box['height'], message_bounding_box['y'] + message_bounding_box['height'])
                combined_width = combined_right - combined_left
                combined_height = combined_bottom - combined_top

                page.screenshot(path=f"{self.image_path}/reddit_{nb}.png", clip={
                    "x": combined_left,
                    "y": combined_top,
                    "width": combined_width,
                    "height": combined_height
                })

                nb += 1


            browser.close()
        return title_text, comments_list
