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
                    
                new_zip_files = []
                for future in as_completed(futures):
                    new_zip_files.extend(future.result())

            zip_files = new_zip_files
            total_files += len(zip_files)

        end_time = time.time()
        if self.wrongs:
            print(f"Arquivos não extraídos: {self.wrongs}")
        print(f"Tempo total para extração: {end_time - start_time:.2f} segundos")

    def __extract_zip(self, zip_file: Path, destination_folder: Path, total_files: int) -> list[Path]:
        message = f"Extração '{zip_file}'..."
        new_zip_files = []
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
                new_zip_files = self.__find_zips_in_folder(destination_folder)
            with self.__lock:
                self.__extracted_count += 1
                progress = (self.__extracted_count / total_files) * 100
                message += f" Completa. Progresso: {self.__extracted_count}/{total_files} ({progress:.2f}%)"
            zip_file.unlink()
        except zipfile.BadZipFile:
            message = f"Error: Não foi possível extrair '{zip_file}'."
            self.wrongs.append(zip_file)
        except Exception as e:
            message = f"Erro ao extrair '{zip_file}': {e}"
            self.wrongs.append(zip_file)
        print(message)
        return new_zip_files

    @staticmethod
    def __find_zips_in_folder(folder: Path) -> list[Path]:
        return list(folder.rglob('*.zip'))
