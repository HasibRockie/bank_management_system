from datetime import datetime

class Bank:
    def __init__(self, name) -> None:
        self.name = name
        self.__users = []
        self.__admins = []
        self.__balance = 0
        self.__loan = 0
        self.loan_feature = True 
        self.__transactions = [] 

    @property
    def users(self):
        return self.__users

    @property
    def admins(self):
        return self.__admins
    
    @property
    def transactions(self):
        return self.__transactions
    
    @property
    def loan(self):
        return self.__loan
    
    @loan.setter
    def loan(self, new_amount):
        self.__loan += new_amount
    
    def add_balance(self, amount):
        self.__balance += amount 

    def withdraw_balance(self, amount):
        self.__balance -= amount 
    
    @property
    def balance(self):
        return self.__balance


    def __repr__(self) -> str:
        return f'Bank: {self.name} - Loan Feature : {self.loan_feature}'
    
class User:
    def __init__(self, bank, username, deposit) -> None:
        self.my_bank = bank  
        self.username = username 
        self.account_no = len(bank.users) + 101
        self.total_amount = 0 
        self.loan = 0
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

    def add_loan(self, loan_amount):
        if self.my_bank.balance > loan_amount and loan_amount <= 2 * self.current_balance:
            self.add_loan = loan_amount
            self.my_bank.loan = loan_amount
            print(f"You have taken a loan of amount {loan_amount}")

        else:
            print(f"Sorry! You're not eligible for loan")


    def __repr__(self) -> str:
        return f'{self.username} - account no: {self.account_no} - total money: {self.total_amount}'
    


class Admin:
    def __init__(self, bank, username) -> None:
        self.my_bank = bank 
        self.username = username
        self.admin_id = len(bank.admins) + 501 

    @property
    def total_bank_balance(self):
        return self.my_bank.balance 

    @property
    def total_loan_amount(self):
        return self.my_bank.loan 
    
    def loan_feature(self, loan_opportunity):
        self.my_bank.loan_feature = loan_opportunity

    def __repr__(self) -> str:
        return f"Admin name : {self.username}, admin-id : {self.admin_id}"

    
a_bank = Bank('Hasib bank')
abc = User(a_bank, 'rockie', 5000)
pqr = User(a_bank, 'nafi', 7000)
pqr.add_loan(5000)
abc.add_loan(1234)
xyz = Admin(a_bank, 'nahee')
print(xyz.total_bank_balance)
print(xyz.total_loan_amount)
xyz.loan_feature(False)


