import requests 
import pandas as pd 
from datetime import datetime 

def fetch_ohlcv_data(tickers, server_url, start_date="2000-01-01", end_date=None):
    print(f"Tickers received in fetch_ohlcv_data: {tickers}")
    if not tickers or not server_url:
        print("Error: Tickers list and server_url must not be empty.")
        return None
        
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
        
    params = {
        "start_date": start_date,  # Fixed: dynamically use the start_date parameter
        "end_date": end_date,
        "securities": tickers
    }
    
    try:
        response = requests.get(server_url, params=params)
        response.raise_for_status() 
        
        data = response.json()
        if not data:
            print("Error: No data returned from the API.")
            return None
            
        df = pd.DataFrame(data)
        df = df.rename(columns={
            "symbol": "Id",
            "date": "MARKETDATE",
            "open": "AdjOPEN_LOC",
            "high": "AdjHIGH_LOC",
            "low": "AdjLOW_LOC",
            "close": "AdjClose_LOC",
            "volume": "AdjVol"
        })
        
        df['MARKETDATE'] = pd.to_datetime(df['MARKETDATE'])
        required_columns = ['MARKETDATE', 'Id', 'AdjOPEN_LOC', 'AdjHIGH_LOC', 'AdjLOW_LOC', 'AdjClose_LOC', 'AdjVol']
        df = df[required_columns]
        
        tickers_with_data = df['Id'].unique()
        print(f"Data successfully fetched for the following tickers: {tickers_with_data.tolist()}")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch OHLCV data from API: {e}")
        return None
    except ValueError as e:
        print(f"Data processing error: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected API response format, missing key: {e}")
        return None

# ==========================================
# TEST IMPLEMENTATION FOR 5 TICKERS
# ==========================================
if __name__ == "__main__":
    # 1. Define your 5 sample tickers
    test_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    
    # 2. Define your API endpoint url (Replace with your actual local or remote container URL)
    # If running inside Docker, use 'http://localhost:8000/api' or your specific service URL
    api_url = "http://10.10.0.6:8000/ohlcv_historic_data" 
    
    print("--- Starting Test ---")
    result_df = fetch_ohlcv_data(
        tickers=test_tickers, 
        server_url=api_url, 
        start_date="2025-01-01"
    )
    
    # 3. View the resulting DataFrame
    if result_df is not None:
        print("\n--- First 5 rows of retrieved data ---")
        print(result_df.head())
    else:
        print("\n--- Test Failed: No DataFrame returned ---")
