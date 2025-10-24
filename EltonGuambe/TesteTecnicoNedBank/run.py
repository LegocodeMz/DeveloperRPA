import os
from data_processing.data_processing import DataProcessing
import constants as const
from data_extraction.data_download import DataDownload



data = DataDownload()
data.download_file(const.BASE_URL)

processor = DataProcessing(const.file_path)
processor.read_file()        # Ler e extrair dados
processor.validate_data()    # Validar registros

processor.save_to_csv(const.output_csv)
