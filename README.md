# BCT IA1: NotesApp
The aim of a note-taking app is to provide users with a digital platform to easily and efficiently capture, organize, and manage their notes and information

> Team Members
1. Sanyukta Joshi (16010120019)
2. Ishika De (16010120065)
3. Tanvi Deshpande (16010120067)

![image](https://github.com/IshikaDe-2803/BCT-IA1/assets/81436870/6257f146-a039-4faf-8e90-feb766b584b9)

> Features
1. Login/Sign Up
2. Note creation 
3. Note deletion
4. Search functionality to search for a particular note
5. Sort notes based on date time

# Tech Stack
- Front End: HTML, CSS, JavaScript
- Back End: Flask
- Blockchain: Ganache (Personal Blockchain), Truffle Framework (Ethereum Smart contracts), Solidity

# Prerequisite
- Download Ganache - https://trufflesuite.com/ganache/
- Install node - https://nodejs.org/en
  
# Installation and Set up
- ```npm install```
- ```cd NotesApp_Flask```
- ```python3 -m venv venv```
- ```venv\Scripts\activate```
- ```pip install -r requirements.txt```

# Set Up Truffle contract
- Open Ganache
- ```truffle compile```
- ```truffle migrate --reset```

# Connecting app to ganache
- Copy the network address from Notes.json and paste it in contract_address in static.py
- From Notes.json, find the transactionHash and search for the same on ganache
- Copy senders_address from ganache and replace the transaction_from parameter in every contract function written in the main app

# Run Flask App
- ```cd NotesApp_Flask```
- ```flask --app notes_app run```

# References
- Creating blockchain app from scratch: https://www.dappuniversity.com/articles/blockchain-app-tutorial
- Connecting Flask to smart contract: https://coinsbench.com/how-to-connect-flask-app-to-a-smart-contract-4a843b0a97fd
- Flask: https://flask.palletsprojects.com/en/2.3.x/installation/#install-flask

