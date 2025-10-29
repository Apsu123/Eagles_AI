import os
import requests
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_image(image_url, download_dir, idx):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 429:
            print(f"Rate limit hit for {image_url}, waiting 5 seconds...")
            import time
            time.sleep(5)
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


def get_images(search, num_results, download_dir, max_workers=8):
    ddgs = DDGS()
    results = ddgs.images(
        keywords=search,
        region="wt-wt",
        safesearch="off",
        max_results=num_results,
    )

    download_tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, result in enumerate(results):
            image_url = result.get("image")
            if image_url:
                future = executor.submit(download_image, image_url, download_dir, idx)
                download_tasks.append(future)
        for future in as_completed(download_tasks):
            pass  # Output handled in download_image


get_images(
    "exotic nature wallpapers 4k pc",
    500,
    "/home/apsu/exotic nature",
)
