import os
import requests
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_image(image_url, download_dir, idx):
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


def get_images(search, num_results, download_dir, id, max_workers=8):
    ddgs = DDGS()
    results = ddgs.images(
        keywords=search,
        region="wt-wt",
        safesearch="off",
        max_results=num_results,
        size="Wallpaper"
    )

    download_tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, result in enumerate(results):
            name = f"{id}_{idx}"
            image_url = result.get("image")
            if image_url:
                future = executor.submit(download_image, image_url, download_dir, name)
                download_tasks.append(future)
        for future in as_completed(download_tasks):
            pass  # Output handled in download_image


if __name__ == "__main__":

    get_images(
        "empty grey backgrounds -shutterstock -watermark",
        15,
        "/home/apsu/FieldTest/Backgrounds4 (Copy)",
        "grey"
    )
