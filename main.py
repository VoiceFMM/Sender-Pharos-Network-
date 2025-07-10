from web3 import Web3
import random
import requests
from eth_account import Account
from api import PRIVATE_KEY, RPC_URL

def proofTrans(tx,address):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk-UA;q=0.6,uk;q=0.5',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODMxNDk2OTQsImlhdCI6MTc1MTYxMzY5NCwic3ViIjoiMHg5N0ZFNWIxZjVBODRFNjQxZDBkNDhGQjA5Yzk4NTE0Q2JkM0JGMDNhIn0.pD6EvbX-InEgdy0dCAN2MxCaiGNCcsuIqE3S6y1MgPo',
        'content-type': 'application/json',
        'origin': 'https://testnet.pharosnetwork.xyz',
        'priority': 'u=1, i',
        'referer': 'https://testnet.pharosnetwork.xyz/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    json_data = {
        'address': w3.to_checksum_address(address),
        'task_id': 103,
        'tx_hash': tx,
    }
    

    response = requests.post('https://api.pharosnetwork.xyz/task/verify', headers=headers, json=json_data)
    return (f"Transaction {tx} verified( Status: {response.status_code} Response: {response.json()["msg"]})")


w3 = Web3(Web3.HTTPProvider(RPC_URL))


if not w3.is_connected():
    raise Exception("Unable to connect to RPC")

sender_address = w3.eth.account.from_key(PRIVATE_KEY).address

count = int(input("Enter number of transaction, or 0 - random(2,5) transactions: "))
count = random.randint(2,5) if count == 0 else count
valueToSend = float(input("Enter value to send, or 0 - random(0.00001,0.001) transactions: "))
receiver_address = str(input("Enter receiver address, or 0 - to send random addresses: "))

print()
for i in  range(count):
    receiverr_address = w3.to_checksum_address(sender_address) if receiver_address != "0" else Account.create().address
    valueToSend = random.randint(1,100) / 100000 if int(valueToSend) == 0 else valueToSend
    nonce = w3.eth.get_transaction_count(sender_address)
    gas_price = w3.eth.gas_price
    value = w3.to_wei(valueToSend, 'ether')  
    
    tx = {
        'nonce': nonce,
        'to': receiverr_address,
        'value': value,
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': w3.eth.chain_id,
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    trans_hash = w3.to_hex(tx_hash)
    print(f"Transaction {i+1}: to address - {receiverr_address}")
    print(f"\t Transaction {i+1} send: {trans_hash}. Value - {valueToSend}")

    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash,timeout=30)
    except:
         print(f"\t Transaction {i+1} failed: {trans_hash} not added to blochain")
         print("\n")
         continue
    else:
        print(f"\t Transaction {i+1} confirmed: {trans_hash} add to block {receipt['blockNumber']}")
        print(f"\t {proofTrans(trans_hash,sender_address)}")
        print("\n")
