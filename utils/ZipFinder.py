from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class ZipFinder:
    def __init__(self, path: Path, cores: int) -> None:
        self.__root_path = path
        self.__max_workers = cores

    def find_zips(self) -> list[Path]:
        start_time = time.time()

        print('Looking for zip files...')
        zip_files = self.__find_zips(self.__root_path)
        with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:
            future_to_file = {executor.submit(self.__find_zips, subdir): subdir for subdir in self.__root_path.iterdir() if subdir.is_dir()}
            for future in as_completed(future_to_file):
                zip_files.extend(future.result())

        end_time = time.time()
        print(f"Total execution time for finding zips: {end_time - start_time:.2f} seconds")

        total_files = len(zip_files)
        if total_files == 0:
            print("No zip files found.")
            return
        
        return zip_files
        
    @staticmethod
    def __find_zips(root: Path) -> list[Path]:
        return list(root.rglob('*.zip'))