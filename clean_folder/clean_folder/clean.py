import re
import sys
import shutil
from pathlib import Path

JPEG_files = list()
PNG_files = list()
JPG_files = list()
SVG_files = list()

AVI_files = list()
MP4_files = list()
MOV_files = list()
MKV_files = list()

DOC_files = list()
DOCX_files = list()
TXT_files = list()
PDF_files = list()
XLSX_files = list()
PPTX_files = list()

MP3_files = list()
OGG_files = list()
WAV_files = list()
AMR_files = list()

ARCHIVE_files = list()
GZ_files = list()
TAR_files = list()

OTHER_files = list()
UNKNOWN_files = set()
extensions = set()
folders = list()

registered_extensions = {

    "JPEG": JPEG_files,
    "PNG": PNG_files,
    "JPG": JPG_files,
    "SVG": SVG_files,

    "AVI": AVI_files,
    "MP4": MP4_files,
    "MOV": MOV_files,
    "MKV": MKV_files,

    "DOC": DOC_files,
    "DOCX": DOCX_files,
    "TXT": TXT_files,
    "PDF": PDF_files,
    "XLSX": XLSX_files,
    "PPTX": PPTX_files,

    "MP3": MP3_files,
    "OGG": OGG_files,
    "WAV": WAV_files,
    "AMR": AMR_files,

    "ZIP": ARCHIVE_files,
    "GZ": ARCHIVE_files,
    "TAR": ARCHIVE_files
}

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'

TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
    "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name: str) -> str:
    name, *extension = name.split(".")
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W", "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("archives", "video", "audio", "documents", "images", "others"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name

        if not extension:
            OTHER_files.append(new_name)

        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)

            except KeyError:
                UNKNOWN_files.add(extension)
                OTHER_files.append(new_name)


def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ""))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects():
    pass


def get_sorted():
    folder_path = Path(sys.argv[1])
    print(folder_path)
    scan(folder_path)

    for file in JPEG_files:
        handle_file(file, folder_path, "images")
    for file in PNG_files:
        handle_file(file, folder_path, "images")
    for file in JPG_files:
        handle_file(file, folder_path, "images")
    for file in SVG_files:
        handle_file(file, folder_path, "images")

    for file in MP4_files:
        handle_file(file, folder_path, "video")
    for file in AVI_files:
        handle_file(file, folder_path, "video")
    for file in MOV_files:
        handle_file(file, folder_path, "video")
    for file in MKV_files:
        handle_file(file, folder_path, "video")

    for file in DOC_files:
        handle_file(file, folder_path, "documents")
    for file in DOCX_files:
        handle_file(file, folder_path, "documents")
    for file in TXT_files:
        handle_file(file, folder_path, "documents")
    for file in PDF_files:
        handle_file(file, folder_path, "documents")
    for file in XLSX_files:
        handle_file(file, folder_path, "documents")
    for file in PPTX_files:
        handle_file(file, folder_path, "documents")

    for file in MP3_files:
        handle_file(file, folder_path, "audio")
    for file in OGG_files:
        handle_file(file, folder_path, "audio")
    for file in WAV_files:
        handle_file(file, folder_path, "audio")
    for file in AMR_files:
        handle_file(file, folder_path, "audio")

    for file in ARCHIVE_files:
        handle_archive(file, folder_path, "archives")
    for file in ARCHIVE_files:
        handle_archive(file, folder_path, "archives")
    for file in ARCHIVE_files:
        handle_archive(file, folder_path, "archives")

    for file in OTHER_files:
        handle_file(file, folder_path, "others")
    for file in UNKNOWN_files:
        handle_file(file, folder_path, "others")

    remove_empty_folders(folder_path)


if __name__ == '__main__':
    get_sorted()
