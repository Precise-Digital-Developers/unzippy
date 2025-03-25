import os
import zipfile
import tarfile
import gzip
import bz2
import shutil
import argparse

def unzippy(archive_path, output_dir):
    """Extracts an archive to the output directory, handling various archive types."""
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    extracted_path = os.path.join(output_dir, member.filename)
                    if not member.is_dir():
                        zip_ref.extract(member, output_dir)
        elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(output_dir)
        elif archive_path.endswith('.tar.bz2') or archive_path.endswith('.tbz2'):
            with tarfile.open(archive_path, 'r:bz2') as tar_ref:
                tar_ref.extractall(output_dir)
        elif archive_path.endswith('.tar'):
            with tarfile.open(archive_path, 'r') as tar_ref:
                tar_ref.extractall(output_dir)
        elif archive_path.endswith('.gz'):
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(archive_path))[0])
            with gzip.open(archive_path, 'rb') as f_in, open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        elif archive_path.endswith('.bz2'):
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(archive_path))[0])
            with bz2.open(archive_path, 'rb') as f_in, open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        else:
            print(f"Unsupported archive type: {archive_path}")
            return

        print(f"Extracted: {archive_path}")

    except Exception as e:
        print(f"Error extracting {archive_path}: {e}")

def unzippy_recursive(root_dir, output_dir):
    """Recursively extracts archives in a directory."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.zip', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar', '.gz', '.bz2')):
                archive_path = os.path.join(root, file)
                unzippy(archive_path, output_dir)

def flatten_directory(directory):
    """Moves all files from subdirectories to the root directory and removes subdirectories."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(directory, file)
            if source_path != dest_path:
                shutil.move(source_path, dest_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                print(f"Error removing {dir_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Recursively extract archives and flatten a directory.")
    parser.add_argument("input_dir", nargs='?', default=".", help="The input directory containing archives. Defaults to current directory.")
    parser.add_argument("output_dir", nargs='?', default="extracted_files", help="The output directory for extracted files. Defaults to 'extracted_files' in the current directory.")
    args = parser.parse_args()

    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    unzippy_recursive(args.input_dir, args.output_dir)
    flatten_directory(args.output_dir)

if __name__ == "__main__":
    main()