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
        return self.total_amount
    
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
            print(f"Your money successfully withdrawn. Amount : {withdraw_amount}, Current balance : {self.current_balance}")
        
        else:
            print(f"Not enough money! Your current balance : {self.current_balance}")

    def __repr__(self) -> str:
        return f'{self.username} - account no: {self.account_no} - total money: {self.total_amount}'

    
a_bank = Bank('Hasib bank')
abc = User(a_bank, 'rockie', 5000)
pqr = User(a_bank, 'nafi', 7000)
abc.withdraw(3000)
pqr.add_money(15000)
print(abc.current_balance)
print(pqr.current_balance)
print(a_bank.users)
print(a_bank.transactions)
