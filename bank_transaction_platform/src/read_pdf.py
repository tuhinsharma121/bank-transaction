import os
import re
import json
import math
from tabula import read_pdf


class ReadPDF:

    def __init__(self):
        pass

    def parse_pdf(self, folder_name, file_name):
        trans_list, bank_data = self.read_transaction(folder_name, file_name)

        # Code to collect category data
        cat_data = {}
        current_dir = os.path.dirname(__file__)
        cat_file = "bank_transaction_platform/data/bank_cat.json"                          # Category dictionary file and folder name
        with open(cat_file) as f:
            cat_data = json.load(f)
        print(cat_data)
        # End of code to read category
        # Code to read the keys and Balance index
        column_index = bank_data.columns
        key_names = column_index.values.tolist()
        i = - 1
        for key in key_names:
            i += 1
            if key == "Balance" or key == "balance" or key == "BALANCE":
                print("Balance position", i)                                # Position of balance in the data
        # End of Code to read the keys and Balance index

        # Code to convert dataframe into list of lists
        trans_date = bank_data[key_names[0]]                                # Find the transaction date
        balances = bank_data["Balance"]                                     # Find the balance
        processed_transaction = []
        one_trans_test = False
        atomic_transaction = {}
        transaction_detail = ""
        for trans, date, balance in zip(trans_list, trans_date, balances):
            if type(balance) is str or math.isnan(balance) is False:
                    if one_trans_test is True:
                        # Code to find and assign category
                        keywords = self.extract_tags(transaction_detail)
                        category = self.assign_category(keywords, cat_data)
                        atomic_transaction["category"] = category
                        # End of code to find and assign category
                        processed_transaction.append(atomic_transaction)
                        print(atomic_transaction)
                        atomic_transaction = {}
                        if type(date) is str:
                            atomic_transaction["Transaction Date"] = date
                        if type(trans) is str:
                            atomic_transaction["Transaction Details"] = trans
                            transaction_detail = trans
                    else:
                        one_trans_test = True
                        if type(date) is str:
                            atomic_transaction["Transaction Date"] = date
                        if type(trans) is str:
                            atomic_transaction["Transaction Details"] = trans
                            transaction_detail = trans
            elif math.isnan(balance) is True:
                if type(date) is str:
                    atomic_transaction["Transaction Date"] = atomic_transaction["Transaction Date"] + date
                if type(trans) is str:
                    atomic_transaction["Transaction Details"] = atomic_transaction["Transaction Details"] + trans
                    transaction_detail = transaction_detail + trans
        return processed_transaction

    def extract_tags(self, transaction):
        transaction = re.sub(r'[^a-zA-Z]', " ", transaction)
        keywords = []
        if type(transaction) is not float:
            ts = transaction.split(':')
            for tt in ts:
                tags = []
                if type(tt) is not float:
                    tags = tt.split()
                if tags:
                    for tag in tags:
                        if len(tag) > 2:
                            keywords.append(tag)
        print(keywords)
        return keywords

    def assign_category(self, keywords, cat_data):
        category = "other"
        if len(keywords) > 0:
            keywords = [k.lower() for k in keywords]
        if cat_data and keywords:
            for key, values in cat_data.items():
                values = [v.lower() for v in values]
                for kw in keywords:
                    if kw in values:
                        category = key
        print("I am an assigned category", category)
        return category

    def read_transaction(self, folder_name, file_name):
        #print(folder_name + "/" + file_name)
        bank_data = read_pdf(folder_name + "/" + file_name, pages='all', nospreadsheet='True')
        max_col = self. find_max(bank_data)
        return list(bank_data[max_col]), bank_data

    def find_max(self, bank_data):
        temp = bank_data.select_dtypes(include='object')
        max_len = 0
        max_col = ''
        for column in temp:
            if temp[column].str.len().max() > max_len:
                max_len = temp[column].str.len().max()
                max_col = column
        return max_col

    def categorize_transaction(self):
        pass

    def list_files(self, folder_path):
        file_list = os.listdir(folder_path)
        return file_list

    def parse_all(self, folder_name):
        file_list = self.list_files(folder_name)
        transaction_list = []
        for file_name in file_list:
            tran_list, bank_data = self.read_transaction(folder_name, file_name)
            print(tran_list)
            if type(tran_list) is list and len(tran_list) > 0:
                transaction_list.append(tran_list)
        return transaction_list
