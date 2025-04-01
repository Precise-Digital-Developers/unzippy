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

        print(f"Extracted: {archive_path} to {output_dir}")

    except Exception as e:
        print(f"Error extracting {archive_path}: {e}")

def unzippy_recursive(root_dir):
    """Recursively extracts archives in a directory to their containing folder."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.zip', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar', '.gz', '.bz2')):
                archive_path = os.path.join(root, file)
                # Extract to the directory containing the archive
                output_dir = os.path.dirname(archive_path)
                unzippy(archive_path, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Recursively extract archives to their containing folders.")
    parser.add_argument("input_dir", nargs='?', default=".", help="The input directory containing archives. Defaults to current directory.")
    args = parser.parse_args()

    args.input_dir = os.path.abspath(args.input_dir)

    unzippy_recursive(args.input_dir)
    print(f"Extraction complete. All archives have been extracted to their containing folders.")

if __name__ == "__main__":
    main()