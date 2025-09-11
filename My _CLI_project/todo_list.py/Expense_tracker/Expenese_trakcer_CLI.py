import os, time
from datetime import datetime


def timer():
  time.sleep(3)
  os.system('cls')


filename = "balance.text"
logfile = "log.expenses.text"
logininfo = "login.file.txt"



def balance_create():
  if os.path.exists(filename):
    with open(filename, "r") as file:
      content = file.read().strip()
      if content == "":
        print("Balance file is empty. Resetting...")  
        os.remove(filename)
        return balance_create()
      try:
        return int(content)
      except ValueError:
        print("Balance file is corrupted. Resetting...")
        os.remove(filename)
        return balance_create()

  else:
    while True:
      try:
        balance = int(
            input(
                "How much do you currently have and want to keep track with?: "
            ))
        print(f"Great you have {balance} to keep track with")

        with open(filename, "w") as file:
          file.write(str(balance))

        now = datetime.now().strftime("%d-%m-%Y - %H:%M")
        with open(logfile, "a") as log:
          log.write(f"{now} - {balance}\n")
        return balance

      except ValueError:
        print("Invalid input")
        timer()


def main_menu():
  print("\nMain Menu\n")
  print("This is an expense tracker app\n")
  print("You can track your daily expenses and income here\n")
  print("You can see your transaction history and view your current balance\n")
  balance_create()
  enter = input("press enter to continue.")
  if enter == "":
    timer()
  balance = balance_create()

  while True:
    print("\nWhat do you want to do?\n")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Check balance")
    print("4. History")
    print("5. Reset")
    print("6. Exit\n")

    Choice = input("> ").lower()

    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    if Choice == "add income" or Choice == "1":
      income = int(input("Please enter your amount: "))
      balance += income
      with open(logfile, "a") as log:
        log.write(str(f"\n{now}: (+${income})"))

      with open(filename, "w") as file:
        file.write(str(balance))
      print(
          f"you have added \033[32m{income}\033[0m, Your new Balance is \033[32m{balance}\033[0m"
      )
      timer()

    elif Choice == "add expense" or Choice == "2":
      expense = int(input("Please enter your amount: "))
      balance -= expense
      with open(logfile, "a") as log:
        log.write(str(f"\n{now}:  (-${expense})"))

      with open(filename, "w") as file:
        file.write(str(balance))

        print(
            f"you spend \033[31m{-expense}\033[0m, Your New Balance is \033[32m{balance}\033[0m"
        )
        timer()

    elif Choice == "check balance" or Choice == "3":
      print(f"Your Current balance is \033[32m{balance}\033[0m")
      timer()

    elif Choice == "history" or Choice == "4":
      print("\nYour Transaction history\n")
      if os.path.exists(logfile):
        with open(logfile, "r") as log:
          print(log.read())
          input("Press enter to continue...")
          os.system('cls')
      else:
        print("There in no Transaction History")
        timer()

    elif Choice == "reset" or Choice == "5":
      choice2 = input(
          "are you sure to reset your balance and history? (yes/no): ")
      if choice2 == "yes":
        if os.path.exists(filename):
          os.remove(filename)
        if os.path.exists(logfile):
          os.remove(logfile)
        print("Your balance has been reset")
        timer()
        balance = balance_create()

    elif Choice == "exit" or Choice == "6":
      print("Thanks you for using this app")
      break

    else:
      print("Please enter Valid option")
      timer()
      continue


def login():

  attempts = 0
  if os.path.exists(logininfo):
    with open(logininfo, "r") as file:
      lines = file.readlines()
    if len(lines) == 2:

      saved_user = lines[0].strip()
      saved_password = lines[1].strip()

      while attempts < 3:
        print("\nNow you can Login")
        print("\nEnter your username")
        username = (input("> "))
        print("Enter your password")
        Password1 = (input("> "))

        if username == saved_user and Password1 == saved_password:
          print("You have logged in successfully!")
          print(f"\nWelcome Back {saved_user}, How are you today?😃")
          timer()
          main_menu()
          return
        else:
          print("Incrroct username or password")
          time.sleep(1)
          os.system('clear')
          attempts += 1
          if attempts == 3:
            print(
                "You have reached maximum number of attempts.\n Now create an account."
            )
            timer()
            create_account()

    else:
      print("Login file is corrupted. Please create a new Account.")
      os.remove(logininfo)
      create_account()


def create_account():
  while True:
    print("Create an New account")

    user = input(f"\nCreate a username: ")
    if len(user) > 15:
      print("Your username can't be more than 15 characters!")
      continue

    print(f"Welcome {user}!")
    print(f"\nCreate a password, {user}")
    password = (input("> "))
    if len(password) > 8:
      print("Password need to be less than 8 chracters!")
      continue
    print(f"{user}, your account has been created\n")


    with open(logininfo, 'a')as f:
     f.write(f"{user}\n{password}")
     print("-" * 15)

    print(f"{user}, Your account as been created successfully!")
    timer()
    main_menu()
    return


print("Welcome to the Income tracking app\n")
choice = input("Do you have an Account?(yes/no): ").lower()
if choice == "yes":
  timer()
  login()
else:
  print("You need to create an account")
  timer()
  create_account()