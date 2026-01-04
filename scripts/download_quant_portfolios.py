import requests
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_quant_files():
    base_url = "https://quantmutual.com/Admin/disclouser/quant_MF_Monthly_Portfolio_{}_{}.xlsx"
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    years = range(2020, 2026)
    
    target_dir = "data/holdings_excel"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    for year in years:
        for month in months:
            # Skip future months in 2026 (not in range, but safe)
            # Current time is Jan 2026
            if year == 2026 and month != "Jan":
                continue
            
            file_name = f"quant_MF_Monthly_Portfolio_{month}_{year}.xlsx"
            url = base_url.format(month, year)
            target_path = os.path.join(target_dir, file_name)
            
            if os.path.exists(target_path):
                logging.info(f"File already exists: {file_name}")
                continue
                
            logging.info(f"Checking URL: {url}")
            try:
                # Use a timeout and a realistic User-Agent
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    with open(target_path, 'wb') as f:
                        f.write(response.content)
                    logging.info(f"Successfully downloaded: {file_name}")
                    # Be nice to the server
                    time.sleep(1)
                elif response.status_code == 404:
                    logging.warning(f"File not found (404): {file_name}")
                else:
                    logging.error(f"Failed to download {file_name}. Status code: {response.status_code}")
            except Exception as e:
                logging.error(f"Error downloading {file_name}: {e}")

if __name__ == "__main__":
    download_quant_files()
