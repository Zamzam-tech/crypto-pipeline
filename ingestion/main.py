from crypto_ingestion import cleanup_old_files, fetch_coin_gecko, load_crypto_data

if __name__=="__main__":
    fetch_coin_gecko()
    load_crypto_data()
    cleanup_old_files()