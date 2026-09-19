"""
Run this script ONCE after setting up Cloudinary to upload all local
product images to Cloudinary cloud storage.

Usage:
  python upload_to_cloudinary.py

Requirements:
  - Set CLOUDINARY_URL in .env file first
  - Run: python upload_to_cloudinary.py
"""
import os
import json
import cloudinary
import cloudinary.uploader
from decouple import config

# Load Cloudinary config from .env
CLOUDINARY_URL = config("CLOUDINARY_URL", default="")
if not CLOUDINARY_URL:
    print("ERROR: CLOUDINARY_URL not set in .env file!")
    print("Get it from: https://console.cloudinary.com/")
    exit(1)

cloudinary.config(cloudinary_url=CLOUDINARY_URL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
FIXTURE_PATH = os.path.join(BASE_DIR, "fixtures.json")

# Load fixture
with open(FIXTURE_PATH, encoding="utf-8") as f:
    data = json.load(f)

print(f"Uploading product images to Cloudinary...")
print("-" * 50)

success = 0
failed = 0

for item in data:
    if item["model"] == "shop.productimage":
        image_field = item["fields"].get("image", "")
        if not image_field:
            continue
        
        local_path = os.path.join(MEDIA_DIR, image_field)
        
        if not os.path.exists(local_path):
            print(f"  SKIP (not found): {image_field}")
            continue
        
        # public_id = folder/filename without extension
        folder = os.path.dirname(image_field)  # "products"
        filename = os.path.splitext(os.path.basename(image_field))[0]
        public_id = f"{folder}/{filename}"
        
        try:
            result = cloudinary.uploader.upload(
                local_path,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            print(f"  OK: {image_field} -> {result['secure_url']}")
            success += 1
        except Exception as e:
            print(f"  FAIL: {image_field} - {e}")
            failed += 1

print("-" * 50)
print(f"Done! {success} uploaded, {failed} failed.")
print()
print("Next steps:")
print("1. Add CLOUDINARY_URL to Render environment variables")
print("2. git add fixtures.json upload_to_cloudinary.py")
print("3. git push -> Render will auto-deploy with product data")
