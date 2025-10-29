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


def get_images_with_colors(serials_path, output_dir, max_workers=8, colors_path=None):
    # Preload colors and serials
    if not colors_path is None:
        with open(colors_path, 'r') as file:
            colors = [line.strip() for line in file if line.strip()]
    else:
        colors = []
    with open(serials_path, 'r') as file:
        serials = [line.strip() for line in file if line.strip()]

    positive = True
    count = 0
    ddgs = DDGS()
    download_tasks = []

    if "neg" in serials_path:
        positive = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for line in serials:
            color = colors[count] if count < len(colors) else None
            download_dir = os.path.join(output_dir, f"NEG{line}" if not positive else line)
            os.makedirs(download_dir, exist_ok=True)

            # Search
            results = ddgs.images(
                keywords=f"lego part {line} images white background",
                region="wt-wt",
                safesearch="off",
                color=color,
                max_results=3,
            )

            if not results:
                # Try a more generic query if no results
                print(f"No images found for '{line}' with color '{color}'. Trying generic search...")
                results = ddgs.images(
                    keywords=f"lego {line}",
                    region="wt-wt",
                    safesearch="off",
                    color=color,
                    max_results=3,
                )
                if not results:
                    print(f"Still no images found for '{line}'. Skipping.")
                    count += 1
                    continue

            # Submit download tasks in parallel
            for idx, result in enumerate(results):
                image_url = result.get("image")
                if image_url:
                    future = executor.submit(download_image, image_url, download_dir, idx)
                    download_tasks.append(future)
            count += 1

        # Wait for all downloads to finish
        for future in as_completed(download_tasks):
            pass  # All output is handled in download_image

def get_images_with_colors2(serials_path, output_dir, max_workers=8, colors_path=None):
    # Preload colors and serials
    if not colors_path is None:
        with open(colors_path, 'r') as file:
            colors = [line.strip() for line in file if line.strip()]
    else:
        colors = []
    with open(serials_path, 'r') as file:
        serials = [line.strip() for line in file if line.strip()]

    positive = True
    count = 0
    ddgs = DDGS()
    download_tasks = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for line in serials:
            color = colors[count] if count < len(colors) else None
            download_dir = output_dir
            os.makedirs(download_dir, exist_ok=True)

            # Search
            results = ddgs.images(
                keywords=f"LEGO part {line} images",
                region="wt-wt",
                safesearch="off",
                color=color,
                max_results=1,
            )

            if not results:
                # Try a more generic query if no results
                print(f"No images found for '{line}' with color '{color}'. Trying generic search...")
                results = ddgs.images(
                    keywords=f"lego {line}",
                    region="wt-wt",
                    safesearch="off",
                    color=color,
                    max_results=5,
                )
                if not results:
                    print(f"Still no images found for '{line}'. Skipping.")
                    count += 1
                    continue

            # Submit download tasks in parallel
            for idx, result in enumerate(results):
                image_url = result.get("image")
                name = f"{line}_{idx}"
                if image_url:
                    future = executor.submit(download_image, image_url, download_dir, name)
                    download_tasks.append(future)
            count += 1

        # Wait for all downloads to finish
        for future in as_completed(download_tasks):
            pass  # All output is handled in download_image



if __name__ == "__main__":
    """
        get_images_with_colors(
            colors_path='/home/apsu/FieldTest/colors.txt',
            serials_path='/home/apsu/FieldTest/serials.txt',
            output_dir="/home/apsu/FieldTest"
        )
    """