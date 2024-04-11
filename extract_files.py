from config.config import CPU_CORES
from utils.Extractor import Extractor
from utils.ZipFinder import ZipFinder
from pathlib import Path
import time

if __name__ == '__main__':
    try:
        start_time = time.time()
        root_path = Path(input('Por favor, insira o caminho completo a ser descompactado:\n').replace('"', ''))

        if root_path.is_file() and root_path.suffix == '.zip':
            zips = [root_path]
        elif root_path.is_dir():
            finder = ZipFinder(root_path, CPU_CORES)
            zips = finder.find_zips()
        else:
            raise ValueError("O caminho fornecido não é reconhecido como um arquivo .zip nem como um diretório.")

        if zips:
            extractor = Extractor(CPU_CORES)
            extractor.extract(zips)


        end_time = time.time()
        total_time = (end_time - start_time)/60.0
        print(f"Extração completa com sucesso. Tempo total de execução: {total_time:.2f} minutos.")

    except Exception as e:
        raise e