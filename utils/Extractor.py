import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading

class Extractor:

    def __init__(self, cores: int) -> None:
        self.__lock = threading.Lock()
        self.__extracted_count = 0
        self.__max_workers = cores
        self.wrongs = []

    def extract(self, zip_files: list[Path]) -> None:
        start_time = time.time()
        total_files = len(zip_files)

        while zip_files:
            futures = []
            with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:
                for zip_file in zip_files:
                    destination_folder = zip_file.parent / zip_file.stem
                    futures.append(executor.submit(self.__extract_zip, zip_file, destination_folder, total_files))
                    
                new_zip_files = [Path]
                for future in as_completed(futures):
                    new_zip_files.extend(future.result())

            for folder in {zip_file.parent for zip_file in new_zip_files}:
                new_zip_files.extend(self.__find_zips_in_folder(folder))

            zip_files = new_zip_files
            total_files += len(zip_files)

        end_time = time.time()
        print(f"Not extracted files: {self.wrongs}")
        print(f"Total execution time for extracting zips: {end_time - start_time:.2f} seconds")

    def __extract_zip(self, zip_file: Path, destination_folder: Path, total_files: int) -> list[Path]:
        message = f"Extracting '{zip_file}'..."
        new_zip_files = []
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
                new_zip_files = [destination_folder / name for name in zip_ref.namelist() if name.endswith('.zip')]
            with self.__lock:
                self.__extracted_count += 1
                progress = (self.__extracted_count / total_files) * 100
                message += f" Done. Progress: {self.__extracted_count}/{total_files} ({progress:.2f}%)"
        except zipfile.BadZipFile:
            message = f"Error: Could not extract '{zip_file}' because it's a bad zip file."
            self.wrongs.append(zip_file)
        except Exception as e:
            message = f"Error extracting '{zip_file}': {e}"
            self.wrongs.append(zip_file)
        print(message)
        return new_zip_files

    @staticmethod
    def __find_zips_in_folder(folder: Path) -> list[Path]:
        return list(folder.rglob('*.zip'))
