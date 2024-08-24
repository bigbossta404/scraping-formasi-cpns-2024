import requests
import pandas as pd
from tqdm import tqdm

# Base URL dan parameter awal
base_url = "https://api-sscasn.bkn.go.id/2024/portal/spf"
params = {
    "kode_ref_pend": "5101087",
    # "pengadaan_kd": 2,
    "offset": 0
}

# Header HTTP untuk permintaan API
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "api-sscasn.bkn.go.id",
    "Origin": "https://sscasn.bkn.go.id",
    "Referer": "https://sscasn.bkn.go.id/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

def view_total_data_only():
    # Melihat total data tanpa melakukan fetching
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "meta" in data["data"]:
            total_records = data["data"]["meta"]["total"]
            print(f"==========================================")
            print(f"Total records available: {total_records}")
            print(f"==========================================")
        else:
            print("No data found in the initial response.")
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")

def fetch_and_export_data():
    # Melakukan fetching data dan ekspor ke file Excel
    all_records = []

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "meta" in data["data"]:
            total_records = data["data"]["meta"]["total"]
            records_per_page = len(data["data"]["data"])
            all_records.extend(data["data"]["data"])  

            # Menghitung jumlah iterasi (dalam kelipatan 10, karena offsetnya 10)
            num_iterations = (total_records // 10)

            with tqdm(total=num_iterations, desc="Fetching Data", unit="page") as pbar:
                # Loop untuk fetching data berdasarkan offset
                for offset in range(10, total_records + 10, 10):
                    params["offset"] = offset
                    print(f"Fetching data at offset: {offset}") 

                    response = requests.get(base_url, headers=headers, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        if "data" in data and "data" in data["data"]:
                            all_records.extend(data["data"]["data"])
                        else:
                            print(f"No more data found at offset {offset}.")
                            break
                    else:
                        print(f"Failed to fetch data at offset {offset}, status code: {response.status_code}")
                        break
                    
                    # Update progress bar
                    pbar.update(1)

            # Konversi data ke DataFrame
            df = pd.DataFrame(all_records)

            # Tambahkan kolom link detail berdasarkan formasi_id
            df['detail_link'] = df['formasi_id'].apply(lambda x: f"https://sscasn.bkn.go.id/detailformasi/{x}")

            # Ekspor ke file Excel
            df.to_excel("api_data_with_links.xlsx", index=False)

            print(f"Data exported successfully to 'api_data_with_links.xlsx'. Total records: {len(all_records)}")
        else:
            print("No data found in the initial response.")
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")

# Menu utama
def main_menu():
    print("Menu:")
    print("1. Lihat jumlah formasi")
    print("2. Fetch and export data")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        view_total_data_only()
    elif choice == '2':
        fetch_and_export_data()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main_menu()
