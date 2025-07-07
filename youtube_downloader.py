import subprocess
import os
import re

def sanitize_filename(name):
    # Removes characters not allowed in file names
    return re.sub(r'[\\/*?:"<>|]', '', name)

def download_highest_quality(url, base_folder='YouTube_Videos'):
    try:
        # Create folder if it doesn't exist
        os.makedirs(base_folder, exist_ok=True)

        # Step 1: Get video title and quality info first
        result = subprocess.run(
            ['yt-dlp', '--get-title', '--get-format', '--no-playlist', url],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().split('\n')
        title = sanitize_filename(lines[0])
        quality_line = lines[1]
        quality_match = re.search(r'\b(\d{3,4}p)\b', quality_line)
        quality = quality_match.group(1) if quality_match else "best"

        filename = f"{title}_{quality}.mp4"
        output_path = os.path.join(base_folder, filename)

        # Step 2: Download the best video+audio and merge to MP4
        command = [
            'yt-dlp',
            '-f', 'bv+ba/b',
            '--merge-output-format', 'mp4',
            '-o', output_path,
            url
        ]
        subprocess.run(command, check=True)
        print(f"✅ Downloaded: {filename}")

    except subprocess.CalledProcessError as e:
        print(f"❌ yt-dlp failed: {e}")
    except Exception as e:
        print(f"❌ General error: {e}")

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ").strip()
    download_highest_quality(video_url)
