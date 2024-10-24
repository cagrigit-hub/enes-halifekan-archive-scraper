from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time
import psycopg
 
 

def insert_tweet(tweets):
    with psycopg.connect(f"host={os.getenv("PG_HOST")} dbname={os.getenv("PG_DATABASE")} user={os.getenv("PG_USER")} password={os.getenv('PG_PASSWORD')}") as conn:
        with conn.cursor() as cur:
            # Insert the tweets into the database on one transaction
            cur.execute('BEGIN;')
            for tweet in tweets:
                cur.execute('INSERT INTO tweets (content) VALUES (%s);', (tweet,))
            cur.execute('COMMIT;')
            conn.commit()
            cur.close()
    print("Tweets inserted into the database successfully")
def scrape_tweets():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://x.com/i/flow/login")
        # fill from env
        page.fill('input[type="text"]', os.getenv('TWITTER_USERNAME'))
        #click the Next button
        print("username entered")
        page.click('#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div > div > div > button:nth-child(6)')
        print("btn clicked")

        # wait for a second
        time.sleep(1)

        # # if search for input[type=text] if it is found fill another
        # if page.query_selector('input[type="text"]') is not None:
        #     print("email found")
        #     page.fill('input[type="text"]', os.getenv('TWITTER_EMAIL'))
        #     print("email entered")
        #     #click the Next button
        #     page.click("#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-1f0wa7y > div > div > div > button")
        #     print("btn clicked")
        # fill in the password

        page.fill('input[type="password"]', os.getenv('TWITTER_PASSWORD'))
        print("password entered")
        #click the Next button
        page.click('#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-1f0wa7y > div > div.css-175oi2r > div > div > button')
        print("btn clicked")
        time.sleep(1)
        
        vc = input("Enter the verification code: ")
        page.fill('input[type="text"]', vc)
        print("vc entered")
        #click the Next button
        page.click("#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-1f0wa7y > div > div > div > button")
        print("btn clicked")
        # wait for a second
        time.sleep(1)
        print("crawler started")

        page.goto('https://x.com/cennet_dunya')

        # Wait for the tweets to load by waiting for the 'article' elements to appear
        page.wait_for_selector('div[data-testid="tweetText"]', timeout=10000)  # Wait for up to 10 seconds
        last_height = page.evaluate('document.body.scrollHeight')
        while True:
            # Scroll to the bottom
            page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
            page.wait_for_timeout(2000)  # Wait for new tweets to load

            # Locate and extract all tweets
            tweets = page.locator('div[data-testid="tweetText"] span').all_inner_texts()  # Simplified the XPath
            if len(tweets) == 0:
                print("No more tweets to load")
                break
            print(f"Extracted {len(tweets)} tweets")
            insert_tweet(tweets)
            # Check if scrolling has reached the bottom of the page
            new_height = page.evaluate('document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        browser.close()

if __name__ == '__main__':
    start = time.time()
    load_dotenv()
    scrape_tweets()
    end = time.time()

    print(f"Time taken: {end - start} seconds")
