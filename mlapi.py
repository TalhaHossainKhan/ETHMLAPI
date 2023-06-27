from fastapi import FastAPI
import pickle
import requests
from datetime import datetime


app = FastAPI()
    
@app.get("/")
async def gatherPredict_data(AddressEther:str):
    api_key = "WY5W2MXQZBTUJZET6TQSNS5XXMU1NBBKH1"
    address = AddressEther.lower()

    url = "https://api.etherscan.io/api"

    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "page": 1,
        "offset": 10000,
        "apikey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extracting the relevant information
    transactions = data["result"]

    # Define empty lists to store the extracted data
    timestamps = []
    from_addresses = []
    to_addresses = []
    values = []

    # Iterate over the transactions and extract the desired fields
    for transaction in transactions:
        timestamp_unix = int(transaction["timeStamp"])
        
        # Convert timestamp from Unix time to datetime object
        timestamp = datetime.utcfromtimestamp(timestamp_unix)
        
        from_address = transaction["from"]
        to_address = transaction["to"]
        value_wei = int(transaction["value"])

        # Convert value from wei to ether
        value_ether = value_wei / 10**18

        # Append the extracted data to the respective lists
        timestamps.append(timestamp)
        from_addresses.append(from_address)
        to_addresses.append(to_address)
        values.append(value_ether)

    # Calculate the time difference between adjacent timestamps in minutes
    time_diff_minutes = []
    sent_minute = []
    received_minute = []
    sent_val = []
    received_val = []
    for i in range(1, len(timestamps)):
        curr_time = timestamps[i]
        prev_time = timestamps[i - 1]
        diff = (curr_time - prev_time).total_seconds() / 60
        time_diff_minutes.append(diff)
        
        if from_addresses[i - 1] == address:
            sent_minute.append(diff)
            sent_val.append(values[i-1])
            
        if to_addresses[i - 1] == address: 
            received_minute.append(diff)
            received_val.append(values[i-1])

    # Calculate the average of values in sent_minute and received_minute arrays
    Avg_min_between_sent_tnx = sum(sent_minute) / len(sent_minute) if sent_minute else 0
    Avg_min_between_received_tnx = sum(received_minute) / len(received_minute) if received_minute else 0

    # Store the number of unique elements in from_addresses and to_addresses arrays
    Average_of_Unique_Sent_To_Addresses = len(set(from_addresses))
    Average_of_Unique_Received_From_Addresses = len(set(to_addresses))

    # Store the number of elements in sent_minute and received_minute arrays
    Sent_tnx = len(sent_minute)
    Received_tnx = len(received_minute)

    # Find the minimum, maximum, and average value from sent_val array
    min_val_sent = min(sent_val) if sent_val else 0
    max_val_sent = max(sent_val) if sent_val else 0
    avg_val_sent = sum(sent_val) / len(sent_val) if sent_val else 0
    total_Ether_sent = sum(sent_val)

    # Find the minimum, maximum, and average value from received_val array
    min_value_received = min(received_val) if received_val else 0
    max_value_received = max(received_val) if received_val else 0
    avg_value_received = sum(received_val) / len(received_val) if received_val else 0
    total_ether_received = sum(received_val)

    #Totalling
    total_transactions_including_tnx_to_create_contract = Sent_tnx + Received_tnx
    total_ether_balance = total_ether_received - total_Ether_sent  


    PredictArray = [Avg_min_between_received_tnx, Avg_min_between_sent_tnx, Sent_tnx, Received_tnx, Average_of_Unique_Received_From_Addresses,
               Average_of_Unique_Sent_To_Addresses, min_value_received, max_value_received, avg_value_received, min_val_sent,
               max_val_sent, avg_val_sent, total_transactions_including_tnx_to_create_contract, total_Ether_sent, total_ether_received,
               total_ether_balance]

    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    Predict = model.predict([PredictArray])
        
    return {"Prediction":int(Predict)}



