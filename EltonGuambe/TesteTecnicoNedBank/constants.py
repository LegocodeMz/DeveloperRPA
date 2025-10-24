import os

DATA_URL = "https://rpa.xidondzo.com/docs/GenericReport.txt"
BASE_URL = "https://rpa.xidondzo.com"
FILE_PATH = "data_extraction/downloads/GenericReport.txt"


project_root = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(project_root, "data_extraction", "downloads")
file_path = os.path.join(download_folder, "GenericReport.txt")
output_csv = os.path.join(download_folder, "valid_registros.csv")
