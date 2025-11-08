import time
import pandas as pd
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime
import asyncio
from apify import Actor # <-- Import Apify SDK

# --- KONFIGURASI ---
# SCROLL_PAUSE_TIME bisa diambil dari input
SCROLL_PAUSE_TIME = 5

# --------------------

# Fungsi scrape_tweets Anda (Hampir sama, tapi ubah cara menyimpan data)
async def scrape_tweets(driver, query, target_count, search_type):
    search_url = f"https://x.com/search?q={query}&src=typed_query"
    if search_type == 'latest':
        search_url += "&f=live"

    print(f"Mengunjungi halaman pencarian: {search_url}")
    driver.get(search_url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
        )
        print("Konten tweet terdeteksi.")
    except TimeoutException:
        print("Batas waktu menunggu habis.")
        return 0 # Kembalikan jumlah data yang didapat

    tweets_data = {}
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    tweets_pushed = 0

    while len(tweets_data) < target_count:
        print(f"\nTweet terkumpul sesi ini: {len(tweets_data)}/{target_count}. Melakukan scroll...")
        tweet_articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

        for tweet in tweet_articles:
            try:
                tweet_url_elements = tweet.find_elements(By.XPATH, ".//a[contains(@href, '/status/')]")

                tweet_url = tweet_url_elements[0].get_attribute('href') if tweet_url_elements else None

                if tweet_url and tweet_url not in tweets_data:
                    # Parse tweet data
                    username = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']//span").text
                    handle = tweet.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
                    timestamp = tweet.find_element(By.XPATH, ".//time").get_attribute('datetime')
                    tweet_text = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text.replace('\n', ' ')
                    reply_count = tweet.find_element(By.XPATH, ".//button[@data-testid='reply']").text or "0"
                    retweet_count = tweet.find_element(By.XPATH, ".//button[@data-testid='retweet']").text or "0"
                    like_count = tweet.find_element(By.XPATH, ".//button[@data-testid='like']").text or "0"

                    tweet_item = {
                        "username": username, "handle": handle, "timestamp": timestamp,
                        "tweet_text": tweet_text, "url": tweet_url, "reply_count": reply_count,
                        "retweet_count": retweet_count, "like_count": like_count
                    }

                    tweets_data[tweet_url] = tweet_item

                    # !!! PERUBAHAN UTAMA: Simpan data langsung ke dataset
                    await Actor.push_data(tweet_item)
                    tweets_pushed += 1

            except Exception:
                continue

        if len(tweets_data) >= target_count:
            print(f"Target {target_count} tweet untuk sesi ini telah tercapai.")
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(SCROLL_PAUSE_TIME) # Gunakan asyncio.sleep

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts > 3:
                print("Tidak ada tweet baru. Mengakhiri sesi ini.")
                break
        else:
            scroll_attempts = 0
        last_height = new_height

    return tweets_pushed # Kembalikan jumlah data yang berhasil di-push

# Fungsi get_user_input() TIDAK DIPERLUKAN LAGI
# Fungsi setup_driver() TIDAK DIPERLUKAN LAGI

async def main():
    async with Actor:
        print("Memulai Apify Actor...")

        # !!! PERUBAHAN UTAMA: Dapatkan input dari Actor
        actor_input = await Actor.get_input() or {}

        # Ambil semua parameter dari input
        auth_token = actor_input.get("authTokenCookie")
        keyword = actor_input.get("keyword", "anies")
        target_per_session = actor_input.get("targetPerSession", 100)
        start_date_str = actor_input.get("startDate", "2025-05-01")
        end_date_str = actor_input.get("endDate", "2025-05-10")
        interval = actor_input.get("intervalDays", 1)
        lang = actor_input.get("language", "id")
        search_type = actor_input.get("searchType", "top") # 'top' or 'latest'

        if not auth_token:
            print("Error: Harap isi 'authTokenCookie' di tab Input Actor.")
            await Actor.fail(status_message="authTokenCookie diperlukan.")
            return

        # Konversi tanggal
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

        print("Menyiapkan Selenium Driver yang disediakan Apify...")
        # !!! PERUBAHAN UTAMA: Gunakan browser dari Apify
        driver = await Actor.new_selenium_driver(
            headless=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        print("Driver siap.")

        try:
            # --- Login sekali saja di awal ---
            print("Mengunjungi x.com untuk menyuntikkan cookie login...")
            driver.get("https://x.com")
            await asyncio.sleep(2)

            cookie = {'name': 'auth_token', 'value': auth_token, 'domain': '.x.com'}
            driver.add_cookie(cookie)
            print("Cookie berhasil disuntikkan.")

            total_tweets_pushed = 0
            current_date = start_date

            # --- Loop utama untuk scraping per interval ---
            while current_date <= end_date:
                chunk_end_date = current_date + datetime.timedelta(days=interval)
                since_str = current_date.strftime('%Y-%m-%d')
                until_str = chunk_end_date.strftime('%Y-%m-%d')

                print(f"\n--- MEMULAI SESI: {since_str} hingga {until_str} ---")

                search_query_raw = f"{keyword} lang:{lang} until:{until_str} since:{since_str}"
                search_query = quote(search_query_raw)

                session_data_count = await scrape_tweets(driver, search_query, target_per_session, search_type)
                total_tweets_pushed += session_data_count

                print(f"Sesi {since_str} - {until_str} selesai. Tweet didapat: {session_data_count}")
                print(f"Total tweet terkumpul sejauh ini: {total_tweets_pushed}")

                current_date = chunk_end_date

                if current_date <= end_date:
                    print("Memberi jeda 10 detik sebelum sesi berikutnya...")
                    await asyncio.sleep(10)

            print(f"\n--- SEMUA SESI SELESAI ---")
            print(f"Total tweet unik yang berhasil disimpan: {total_tweets_pushed}")

            # !!! PERUBAHAN UTAMA: Simpan output (opsional, karena data sudah di dataset)
            # Anda bisa menyimpan ringkasan ke Key-Value Store
            await Actor.set_value("OUTPUT", {
                "totalTweets": total_tweets_pushed,
                "keyword": keyword,
                "dateRange": f"{start_date_str} to {end_date_str}"
            })

        finally:
            if driver:
                print("\nMenutup browser...")
                driver.quit()

if __name__ == "__main__":
    asyncio.run(main())