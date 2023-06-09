from datetime import datetime

class Bank:
    def __init__(self, name) -> None:
        self.name = name
        self.__users = []
        self.__balance = 0
        self.__loan = 0
        self.loan_feature = True 
        self.__transactions = [] 

    @property
    def users(self):
        return self.__users
    
    @property
    def transactions(self):
        return self.__transactions
    
    def add_balance(self, amount):
        self.__balance += amount 

    def withdraw_balance(self, amount):
        self.__balance -= amount 
    
    @property
    def balance(self):
        return self.__balance


    def __repr__(self) -> str:
        return f'Bank: {self.name}'
    
class User:
    def __init__(self, bank, username, deposit) -> None:
        self.my_bank = bank  
        self.username = username 
        self.account_no = len(bank.users) + 101
        self.total_amount = 0 
        self.history = []
        self.add_money(deposit) 

    def add_money(self, amount):
        self.total_amount += amount 
        self.history.append({'username': self.username, 'acc_no': self.account_no, 'amount': amount, 'date': datetime.now(), 'transaction_type': "Add Money"})
        self.my_bank.transactions.append({'username': self.username, 'acc_no': self.account_no, 'amount': amount, 'date': datetime.now(), 'transaction_type': "Add Money"})
        for user in self.my_bank.users:
            if user['username'] == self.username and user['acc_no'] == self.account_no:
                user['amount'] = self.total_amount
                self.my_bank.add_balance(amount)
                break
        else:
            self.my_bank.users.append({'username': self.username, 'acc_no': self.account_no, 'amount': self.total_amount})
            self.my_bank.add_balance(amount)

    @property
    def current_balance(self):
        for user in self.my_bank.users:
            if user['username'] == self.username and user['acc_no'] == self.account_no:
                return user['amount']
                break
    
    @current_balance.setter
    def current_balance(self, new_balance):
        self.total_amount = new_balance

    @property
    def transaction_history(self):
        return self.history
    
    def withdraw(self, withdraw_amount):
        if self.total_amount > withdraw_amount:
            self.total_amount -= withdraw_amount
            self.history.append({'username': self.username, 'acc_no': self.account_no, 'amount': withdraw_amount, 'date': datetime.now(), 'transaction_type': "Withdraw Money"})
            self.my_bank.transactions.append({'username': self.username, 'acc_no': self.account_no, 'amount': withdraw_amount, 'date': datetime.now(), 'transaction_type': "Withdraw Money"})
            for user in self.my_bank.users: 
                if user['username'] == self.username and user['acc_no'] == self.account_no:
                    user['amount'] = self.total_amount
                    self.my_bank.withdraw_balance(withdraw_amount)
            print(f"Your money successfully withdrawn. Amount: {withdraw_amount}, Current balance: {self.current_balance}")

        elif withdraw_amount > self.my_bank.balance:
            print(f"Sorry! The bank is bankrupt!")
        
        else:
            print(f"Not enough money! Your current balance: {self.current_balance}")

    def transfer_money(self, receiver_acc, transfer_amount):
        if self.total_amount > transfer_amount:
            for user in self.my_bank.users:
                if user['acc_no'] == receiver_acc:
                    receiver = user
                    break
            else:
                receiver = None

            for user in self.my_bank.users:
                if user['username'] == self.username and user['acc_no'] == self.account_no:
                    user['amount'] -= transfer_amount
                    break 
            
            if receiver and receiver['username'] != self.username:
                receiver['amount'] += transfer_amount
                self.total_amount -= transfer_amount
                self.history.append({'username': self.username, 'acc_no': self.account_no, 'amount': transfer_amount, 'date': datetime.now(), 'transaction_type': "Transfer Money"})
                self.my_bank.transactions.append({'username': self.username, 'acc_no': self.account_no, 'amount': transfer_amount, 'date': datetime.now(), 'transaction_type': "Transfer Money"})
                self.my_bank.transactions.append({'username': receiver['username'], 'acc_no': receiver_acc, 'amount': transfer_amount, 'date': datetime.now(), 'transaction_type': "Added Transferred Money"})
                print(f"Successfully transferred amount {transfer_amount} to the account no.: {receiver_acc}")

            else:
                print(f"Receiver's account not found or cannot transfer money to your own account!")
        else:
            print(f"Not enough money! Your current balance: {self.current_balance}")

    def __repr__(self) -> str:
        return f'{self.username} - account no: {self.account_no} - total money: {self.total_amount}'

    
a_bank = Bank('Hasib bank')
abc = User(a_bank, 'rockie', 5000)
pqr = User(a_bank, 'nafi', 7000)
abc.transfer_money(102, 3500)
for transaction in a_bank.transactions:
    print(transaction)
