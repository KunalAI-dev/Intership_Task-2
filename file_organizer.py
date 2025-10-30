import os
import shutil
import argparse
from datetime import datetime

# -----------------------------
# Function to get timestamped log entry
# -----------------------------
def log(message, log_file):
    with open(log_file, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

# -----------------------------
# Handle file name collisions
# -----------------------------
def get_unique_path(dest_path):
    """Return a unique file path if name collision occurs."""
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = f"{base}_{counter}{ext}"
        counter += 1
    return dest_path

# -----------------------------
# Organize files
# -----------------------------
def organize_files(source_folder, dry_run=False, log_file="organizer.log"):
    if not os.path.exists(source_folder):
        print("❌ Source folder does not exist.")
        return

    log(f"Starting file organization in '{source_folder}' (dry_run={dry_run})", log_file)

    for filename in os.listdir(source_folder):
        src_path = os.path.join(source_folder, filename)

        # Skip directories
        if os.path.isdir(src_path):
            continue

        # Determine file extension
        ext = os.path.splitext(filename)[1].lower().strip(".") or "no_extension"
        target_dir = os.path.join(source_folder, ext.upper())

        # Create target folder if not exists
        if not dry_run and not os.path.exists(target_dir):
            os.makedirs(target_dir)
            log(f"Created folder: {target_dir}", log_file)

        dest_path = os.path.join(target_dir, filename)
        dest_path = get_unique_path(dest_path)

        if dry_run:
            print(f"[DRY-RUN] Would move: {src_path} → {dest_path}")
            log(f"[DRY-RUN] Would move: {src_path} → {dest_path}", log_file)
        else:
            shutil.move(src_path, dest_path)
            print(f"Moved: {src_path} → {dest_path}")
            log(f"Moved: {src_path} → {dest_path}", log_file)

    log("✅ File organization completed.\n", log_file)

# -----------------------------
# Main Entry (CLI)
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files into subfolders by extension.")
    parser.add_argument("path", help="Path to the folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without moving files")
    parser.add_argument("--log", default="organizer.log", help="Log file name")
    args = parser.parse_args()

    organize_files(args.path, dry_run=args.dry_run, log_file=args.log)
