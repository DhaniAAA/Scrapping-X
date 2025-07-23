# X / Twitter Scraper with Selenium
This Python script is designed to scrape tweets from the X platform (formerly Twitter) based on search keywords. The script uses Selenium to automate the browser and mimic user behavior, so it does not require official X API access.

To bypass the frequently appearing login page, this script uses the authentication cookie injection method `(auth_token)`.

# ✨ Features
* Keyword-Based Search: Retrieves tweets based on any search query.
* Login with Cookies: Bypasses the X login page by injecting your auth_token, making the scraping process more reliable.
* Automatic Scrolling: Automatically scrolls down to load more tweets.
* Export to CSV: Saves all successfully retrieved data into a neat .csv file containing columns: `username`, `handle`, `timestamp`, `tweet_text`, `url`, `reply_count`, `retweet_count`, and `like_count`.
* Compatible with Google Colab: Includes a guide for running in the Google Colab environment.

# ⚙️ Requirements
- Python 3.8 or newer.
- Google Chrome browser installed on your computer (unless using Google Colab). `pip` for Python package installation.

# 🚀 Installation & Preparation

Clone This Repository 
```bash
https://github.com/DhaniAAA/Scrapping-X.git
cd YOUR_REPO_NAME
```

Install Required Python Packages
Open the terminal or command prompt in the project folder, then run the following command:
```bash
pip install -r requirements.txt
```
(Ensure you create a `requirements.txt` file containing `pandas`, `selenium`, and `webdriver-manager`)

# 📝 How to Use
The process of using this script consists of three main steps:

Step 1: Obtain Your `auth_token` Cookie
This is the most important step to ensure the script can “log in” to X.

1. Open X.com in your browser: Use Google Chrome, open x.com, and log in to your account.
2. Developer Tools: Press F12 on your keyboard or right-click anywhere and select Inspect.
3. Find the cookie: 
   - In the Developer Tools panel, click the Application tab.
   - In the left menu, under “Storage,” open Cookies -> https://x.com.
   - Look for the cookie with the exact name auth_token.
4. Copy the Value: Click on the auth_token row and copy the entire long text in the “Cookie Value” column.

**STRONG WARNING**: Your auth_token value is **SECRET**, just like a password. Anyone who has it can gain access to your X account. NEVER share your code or files with anyone if this token is still in them.

Step 2: Configure the Script

Open the `Scrapping_x.py` file (or your main file name) and change the variable values at the top:
```bash
# --- CONFIGURATION ---
# 1. PASTE YOUR `auth_token` VALUE HERE
AUTH_TOKEN_COOKIE = “paste_your_auth_token_value_here”
```

Step 3: Run the Script
Return to your terminal or command prompt: 
1. Return to your terminal or command prompt, then run the script:
```bash
python Scrapping_x.py
```
2. The script will prompt you to enter search details one by one. Example:
```bash
#English
1. Enter the keyword/search topic: anies
2. What is the MAXIMUM number of tweets you want to retrieve PER SESSION? 100
3. Enter the OVERALL START DATE (YYYY-MM-DD): 2025-05-01
4. Enter the OVERALL END DATE (YYYY-MM-DD): 2025-06-01
5. How many days should the scraping session interval be? (e.g., 1 for per day): 3
6. Enter the language code (e.g., 'id' for Indonesian, 'en' for English): id
7. Select the tweet type (1 for Top, 2 for Newest): 1

#Indonesia
1. Masukkan kata kunci/topik pencarian: anies
2. Berapa jumlah MAKSIMAL tweet yang ingin diambil PER SESI? 100
3. Masukkan TANGGAL MULAI KESELURUHAN (YYYY-MM-DD): 2025-05-01
4. Masukkan TANGGAL SELESAI KESELURUHAN (YYYY-MM-DD): 2025-06-01
5. Berapa hari interval per sesi scraping? (misal: 1 untuk per hari): 3
6. Masukkan kode bahasa (misal: 'id' untuk Indonesia, 'en' untuk Inggris): id
7. Pilih jenis tweet (1 untuk Top, 2 untuk Terbaru): 1
```

3. After you have filled in all the inputs, the script will start the scraping process. If successful, you will find a `.csv` file (example: `tweets_AniesBaswedan.csv`) in the same folder.
The script will start the process, and if successful, you will find a `tweets_(your search).csv` file in the same folder.

# ☁️ Usage in Google Colab
If you are using Google Colab, you need to run some installation commands in the first cell before running the main script. Cell

# 1. Installing Dependencies# Install Python libraries

```bash
!pip install selenium pandas webdriver-manager
```
# Download and install Google Chrome for the Colab environment
```bash
# Install required Python libraries
!pip install selenium pandas webdriver-manager

# Download and install Google Chrome
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb

# If there are dependency errors, run this command to fix them
!apt-get install -f
```
# 2: Run the Scraper Script 
Once the above cell is complete, you can run the cell containing your Python scraper code. Make sure you have filled in `AUTH_TOKEN_COOKIE` in the code. The script is configured to run in a server environment such as Colab.

⚠️ Disclaimer for this script. 
- This script is created for educational and research purposes. Use it wisely and ethically.
- Platform X actively prevents scraping. This script may stop working at any time if X changes the HTML structure of its site. If that happens, the XPath selectors in the code may need to be updated.
- Excessive scraping may result in your account being temporarily restricted or blocked.
