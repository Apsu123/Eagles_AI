import os
import requests
import time
from duckduckgo_search import DDGS

def backup_images(serials_path, testset_dir):
    with open(serials_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            clean_line = line.strip()
            download_dir = os.path.join(testset_dir, line)
            os.makedirs(download_dir, exist_ok=True)
            results = DDGS().images(
                keywords=f"lego {line} piece",
                region="wt-wt",
                safesearch="off",
                color="",
                max_results=4
            )
            print(f"Results for {line.strip()}: {len(results)}")
            for idx, result in enumerate(results):
                image_url = result.get("image")
                if image_url:
                    try:
                        response = requests.get(image_url, timeout=10)
                        if response.status_code == 200:
                            ext = os.path.splitext(image_url)[1] or ".jpg"
                            filename = f"image_{idx}{ext}"
                            file_path = os.path.join(download_dir, filename)
                            with open(file_path, "wb") as f:
                                f.write(response.content)
                            print(f"Saved: {file_path}")
                        else:
                            print(f"Failed to fetch: {image_url}")
                    except Exception as e:
                        print(f"Error downloading {image_url}: {e}")
            time.sleep(5)

if __name__ == "__main__":
    backup_images('/home/apsu/LegoDetect/serials.txt', "/home/apsu/LegoDetect/TestSet")
