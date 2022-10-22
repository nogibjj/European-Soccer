import os
import kaggle

def download():
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('hugomathien/soccer', path='Data', unzip=True)

if __name__ == '__main__':
    #if file does not exist, download it
    if not os.path.exists('Data/database.sqlite'):
        download()