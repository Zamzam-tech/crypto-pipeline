from crypto_ingestion import cleanup_old_files, fetch_coin_gecko, load_crypto_data
from fear_greed_ingestion import fetch_fear_greed, load_fear_greed

if __name__=="__main__":
    fetch_coin_gecko()
    load_crypto_data()
    cleanup_old_files()
    fetch_fear_greed()
    load_fear_greed()   