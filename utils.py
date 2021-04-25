
from classes import Event
import os
import re
import datetime
import pandas as pd


def parse_file(folder):
    print("######################")
    print("PROCESSING:  ")
    print(folder)
    print("######################")
    list_events=[]
    folder = os.path.join(os.path.dirname(__file__), folder)
    for filename in os.listdir(folder):
        print(filename)
        if "STAKING_FLEX" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                for line in a_file:
                    if not line.startswith("--"):
                        line_parts=re.split(r'\t+',line)
                        e=Event(trans_type="Staking",buy_amt=line_parts[3],buy_cur=line_parts[1],comment="Binance Flexible Staking",effective_date=parse_date(line_parts[0],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                        list_events.append(e)
        if "STAKING_LOCKED" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                for line in a_file:
                    if not line.startswith("--"):
                        try:
                            line_parts=re.split(r'\t+',line)
                            e=Event(trans_type="Staking",buy_amt=line_parts[3],buy_cur=line_parts[0],comment="Binance Locked Staking",effective_date=parse_date(line_parts[4],'%Y-%m-%d'),exchange="Binance")
                            list_events.append(e)
                        except:
                            print("ERROR:")
                            print(line)
                            print(line_parts)
        if "Buy History" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                df = pd.read_excel(filename, sheet_name="sheet1")
                df = df[df["Status"] == "Completed"]
                for index, row in df.iterrows():
                    e=Event(trans_type="Trade",buy_amt=row["Final Amount"].split(" ")[0],buy_cur=row["Final Amount"].split(" ")[1],sell_amt=row["Amount"].split(" ")[0],sell_cur=row["Amount"].split(" ")[1],fee_amt=row["Fees"].split(" ")[0],fee_cur=row["Fees"].split(" ")[1],comment="Binance Buy",effective_date=parse_date(row["Date(UTC)"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    list_events.append(e)
        if "DEPOSIT_HISTORY_FIAT" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                df = pd.read_excel(filename, sheet_name="sheet1")
                df = df[df["Status"] == "Succesfull"]
                for index, row in df.iterrows():
                    e=Event(trans_type="Deposit",buy_amt=row["Amount"],buy_cur=row["Coin"],fee_amt=row["Fee"],fee_cur=row["Coin"],comment="Binance Deposit Fiat",effective_date=parse_date(row["Date(UTC)"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    list_events.append(e)
        if "DEPOSIT_HISTORY_CRYPTO" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                df = pd.read_excel(filename, sheet_name="sheet1")
                df = df[df["Status"] == "Completed"]
                for index, row in df.iterrows():
                    e=Event(trans_type="Deposit",buy_amt=row["Amount"],buy_cur=row["Coin"],comment="Binance Deposit Fiat",effective_date=parse_date(row["Date(UTC)"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    list_events.append(e)
        if "part" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                df = pd.read_csv(filename)
                for index, row in df.iterrows():
                    row["BuyCoin"]=row["Executed"]
                    row["PayCoin"]=row["Amount"]
                    row["FeeCoin"]=row["Fee"]
                    row["Executed"]=row["Executed"][0:len(row["Executed"])-3]
                    row["Amount"]=row["Amount"][0:len(row["Amount"])-3]
                    row["Fee"]=row["Fee"][0:len(row["Fee"])-3]
                    row["BuyCoin"]=row["BuyCoin"].replace(row["Executed"],"")
                    row["PayCoin"]=row["PayCoin"].replace(row["Amount"],"")
                    row["FeeCoin"]=row["FeeCoin"].replace(row["Fee"],"")
                    print(row["Side"])
                    if "BUY" in row["Side"]:
                        e=Event(trans_type="Trade",buy_amt=row["Executed"],buy_cur=row["BuyCoin"],fee_amt=row["Fee"],fee_cur=row["FeeCoin"],sell_amt=row["Amount"],sell_cur=row["PayCoin"],comment="Binance Buy History",effective_date=parse_date(row["Date(UTC)"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    if "SELL" in row["Side"]:
                        e=Event(trans_type="Trade",buy_amt=row["Amount"],buy_cur=row["PayCoin"],fee_amt=row["Fee"],fee_cur=row["FeeCoin"],sell_amt=row["Executed"],sell_cur=row["BuyCoin"],comment="Binance Buy History",effective_date=parse_date(row["Date(UTC)"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    list_events.append(e)
        if "CONVERSIONS_BNB" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                df = pd.read_csv(filename)
                for index, row in df.iterrows():
                    e=Event(trans_type="Trade",buy_amt=row["Converted BNB"],buy_cur="BNB",fee_amt=row["Fee (BNB)"],fee_cur="BNB",sell_amt=row["Amount"],sell_cur=row["Coin"],comment="Binance BNB Conversion low capitals",effective_date=parse_date(row["Date"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    list_events.append(e)
        if "AIRDROPS" in filename:
            filename = os.path.join(folder, filename)
            with open(filename, "r") as a_file:
                df = pd.read_csv(filename)
                for index, row in df.iterrows():
                    e=Event(trans_type="Airdrop",buy_amt=row["Amount"],buy_cur=row["Coin"],comment="Binance Airdrop "+row["Note"],effective_date=parse_date(row["Time"],'%Y-%m-%d %H:%M:%S'),exchange="Binance")
                    list_events.append(e)
                           
                        
    return list_events               


def parse_date(date_arg,date_format):
    date_obj=datetime.datetime.strptime(date_arg, date_format)
    return date_obj.strftime('%m/%d/%Y %H:%M:%S')


def generate_file(events):
    file_output=os.path.join(os.path.dirname(__file__),"Binance_output_"+datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')+".csv")
    with open(file_output, "w+") as a_file:
        a_file.write("Type,Buy Amount,Buy Currency,Sell Amount,Sell Currency,Fee,Fee Currency,Exchange,Trade-Group,Comment,Date\n")
        for event in events:
            a_file.write(event.to_string()+"\n")