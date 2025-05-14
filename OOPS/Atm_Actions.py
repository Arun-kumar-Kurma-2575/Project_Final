import random
class ATM:
    def __init__(self):
        self.id=''
        self.pin=''
        self.balance=0
        for i in range(10):
            self.id+=str(random.randint(0,9))
        self.pin=input('SET your PIN:')
        print(f'PIN set successfully for your bank id {self.id}')
        self.menu()

    def menu(self):
        option=input("""
             Welcome to the  ATM!!!
             click the option  to perform a task
             1- for  CHANGING THE PIN
             2- for  DEPOSIT
             3- for  WITHDRAWING
             4- for  CHECKING THE BALANCE
             5- for  EXIT""")
        if option=='1':
            self.change_pin()
        elif option=='2':
            self.deposit()
        elif option=='3':
            self.withdraw()
        elif option=='4':
            self.check_balance()
        elif option=='5':
            pass
        else: 
            print('Enter the valid option')


    def change_pin(self):
        i=0
        while i<3:
                temp_pin=input("Enter The PIN:")
                if self.pin==temp_pin:
                    self.pin=input("Enter The new PIN:")
                    print(f'PIN changed successfully for your bank id {self.id}')
                    break

                else:
                    if i<3:
                        print('Entered pin is incorrect,Try again')
                    else:
                        print('PIN Entered incorrectly 3 times,limit exceeded')

                i+=1

        if i<3:
            self.menu()
        else:
            print('limit exceeded,Try after some time')

    def  deposit(self):
            i=0
            while i<3:
                temp_pin=input("Enter The PIN:")
                if self.pin==temp_pin:
                    amount=eval(input('Enter the amount you want to deposit:'))
                    self.balance+=amount
                    print('{} deposited successfully into the bank id{}'.format(amount,self.id))
                    break

                else:
                    if i<3:
                        print('Entered pin is incorrect,Try again')
                    else:
                        print('PIN Entered incorrectly 3 times,limit exceeded')

                i+=1

            if i<3:
                self.menu()
            else:
                print('limit exceeded,Try after some time')

    def withdraw(self):
        i=0
        while i<3:
            temp_pin=input("Enter The PIN:")
            if self.pin==temp_pin:
                amount=eval(input('Enter the amount you want to withdraw:'))
                if self.balance < amount:
                    print('Insufficient balance in your account')
                else:
                    self.balance-=amount
                    print('{} withdrawn successfully from the bank id{}'.format(amount,self.id))
                break

            else:
                if i<3:
                    print('Entered pin is incorrect,Try again')
                else:
                    print('PIN Entered incorrectly 3 times,limit exceeded')

            i+=1

        if i<3:
            self.menu()
        else:
            print('limit exceeded,Try after some time')

    def check_balance(self):
        i=0
        while i<3:
            temp_pin=input("Enter The PIN:")
            if self.pin==temp_pin:
                print(f'{self.balance} is the amount present in the bank id {self.id}')
                break

            else:
                if i<3:
                    print('Entered pin is incorrect,Try again')
                else:
                    print('PIN Entered incorrectly 3 times,limit exceeded')

            i+=1

        if i<3:
            self.menu()
        else:
            print('limit exceeded,Try after some time')








