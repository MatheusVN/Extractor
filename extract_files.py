from config.config import CPU_CORES
from utils.Extractor import Extractor
from utils.ZipFinder import ZipFinder
import time

if __name__ == '__main__':
    try:
        start_time = time.time()
        root_path = input('Por favor, insira o caminho completo a ser descompactado:\n')
        finder = ZipFinder(root_path, CPU_CORES)
        extractor = Extractor(CPU_CORES)

        zips = finder.find_zips()

        if zips is not None:
            extractor.extract(zips)


        end_time = time.time()
        total_time = (end_time - start_time)/60.0
        print(f"Extração completa com sucesso. Tempo total de execução: {total_time:.2f} minutos.")

    except Exception as e:
        raise e