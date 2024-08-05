import zipfile


def unzip_file(zip_path, extract_to) -> None:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
