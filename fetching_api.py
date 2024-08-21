import requests
import pandas as pd
from tqdm import tqdm

base_url = "https://api-sscasn.bkn.go.id/2024/portal/spf"
params = {
    "kode_ref_pend": "3000006",
    "pengadaan_kd":2,
    "offset": 0
}

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

all_records = []

response = requests.get(base_url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    if "data" in data and "meta" in data["data"]:
        total_records = data["data"]["meta"]["total"]
        records_per_page = len(data["data"]["data"])
        all_records.extend(data["data"]["data"])  

        # Calculate the total number of iterations  (perkalipatan 10, karena offsetnya 10)
        num_iterations = (total_records // 10)

        with tqdm(total=num_iterations, desc="Fetching Data", unit="page") as pbar:
            # Loop through the offsets in multiples of 10 until all records are fetched
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

        # Convert the list of records to a DataFrame
        df = pd.DataFrame(all_records)

        # Add a new column for the detail preview link based on formasi_id
        df['detail_link'] = df['formasi_id'].apply(lambda x: f"https://sscasn.bkn.go.id/detailformasi/{x}")

        # Export to Excel
        df.to_excel("api_data_with_links.xlsx", index=False)

        print(f"Data exported successfully to 'api_data_with_links.xlsx'. Total records: {len(all_records)}")
    else:
        print("No data found in the initial response.")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")
