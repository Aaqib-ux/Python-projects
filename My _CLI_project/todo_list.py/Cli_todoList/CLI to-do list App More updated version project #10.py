import os,time, csv



to_do_list = []

file_path = "to_do_list.csv"

if os.path.exists(file_path):
    with open(file_path, "r", newline="") as file:
     reader = csv.reader(file)
     next(reader)  # skip header
     to_do_list = [row for row in reader]
else:
  with open(file_path, "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(["Task", "Date", "Priority"])

def add_task():
  time.sleep(1.5)
  os.system("clear")
  Task = input("Enter the task: ").lower().strip()
  date = input("Enter the date: ").strip()
  priority = input("Enter the priority: ").capitalize()
  row = [Task, date, priority]
  to_do_list.append(row)
  with open(file_path, "a") as file:
        writer = csv.writer(file)
        writer.writerow(row)
  print(f"\033[32m{Task}\033[0m --- added to the list")
  input("\npress enter to continue...")
  os.system('clear')

def remove_task():
  time.sleep(1.5)
  os.system("clear")

  Task = input("\nEnter the task to Remove: ").lower().strip()
  found = False
  with open(file_path, "r",newline="") as file:
      reader = csv.reader(file)
      header =  next(reader)
      rows = list(reader)

  update_rows = [row for row in rows if row[0].lower() != Task]

  if len(update_rows) != len(rows):
      found = True
    
  to_do_list[:] = [row for row in to_do_list if row[0].lower() != Task]

  with open(file_path, "w", newline="")as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(update_rows)
        print(f"{Task} Have been removed from the list")

  if found:
      print(f"{Task} Have been removed from the list")
  else:
      print(f"{Task} not found in the list")
  input("\npress enter to continue...")
  os.system('clear')
  view_task()


def view_task():
  time.sleep(1.5)
  os.system('clear')

  if (len(to_do_list)) == 0:
    print("Your list is empty.")
    time.sleep(3)
    os.system("clear")
    return

  task_width = (max(len(row[0]) for row in to_do_list))
  date_width = (max(len(row[1]) for row in to_do_list))
  priority_width = (max(len(row[2]) for row in to_do_list))

  print("\033[34mYour To-Do List\033[0m\n")


  task_width = max(task_width, len("Task"))
  date_width = max(date_width, len("Date"))
  priority_width = max(priority_width, len("priority"))

  print(f"| {'Task'.ljust(task_width)} | {'Date'.ljust(date_width)} | {'priority'.ljust(priority_width)} ")
  print(f"|{'-' * (task_width + 2)}|{'-' * (date_width + 2)}|{'-' * (priority_width +2)}|")

  for row in to_do_list :
    print(f"| {row[0].ljust(task_width)} | {row[1].ljust(date_width)} | {row[2].ljust(priority_width)}")

  print()
  input("Press Enter to continue...")
  os.system("clear")


def edit_task():
  time.sleep(0.5)
  os.system('clear')
  options = {"1":("Task", 0),"2":("Date", 1), "3":("Priority", 2)}

  print("\nWhat you want to edit?\n")
  print("1. Task")
  print("2. Date")
  print("3. Priority")

  choice = input("> ").lower().strip()
  if choice not in options and choice not in ["task", "date", "priority"]:
      print("Imvalid options")
      time.sleep(1.5)
      return

  column_name = None
  col_index = None
  for key,(name,col) in options.items():
    if choice == key or choice == name.lower():
        column_name = name
        col_index = col
        break
  if column_name is None:
      print("Invalid Option")
      time.sleep(1.5)
      return
      
  edited = input(f"Enter the task to edit whose {column_name} you wanna edit: ") 
  found = False


  for i, row in enumerate(to_do_list):
      if row[0].lower() == edited.lower():
        new_value = input(f"Enter the new {column_name}: ").strip()
        if col_index is not None:
           to_do_list[i][col_index] = new_value
           found = True
        break
  if found:
      with open(file_path, "w", newline="") as file:
       writer = csv.writer(file)
       writer.writerow(["Task", "Date", "Priority"])
       writer.writerows(to_do_list)
      print(f"Task '{edited}' has been updated")
  else:
    print(f"Task '{edited}' not found in the list.")


  input("\nPress Enter to continue...")
  os.system("clear")
  view_task()


def filter_task():
  time.sleep(0.5)
  os.system('clear')
  print("filter task:\n")
  print("1. By Date")
  print("2. By priority")
  
  choice = input("> ").lower().strip()
  if choice == "1" or choice == "date":
    date = input("Enter the date (12 aug): ").lower().strip()
    filtered_tasks = [row for row in to_do_list if row[1].lower() == date]
    print(f"\nTasks for {date}:\n")
    for i, task in enumerate (filtered_tasks, 1):
      print(f"{i}. {task[0]} - {task[1]} - {task[2]}")
    input("\n Press Enter to continue...\n")
    os.system('clear')
      
  else:
    priority = input("Enter the priority: ").lower().strip()
    filtered_tasks = [row for row in to_do_list if row[2].lower() == priority]
    print(f"\nTasks for {priority}:\n")
    for task in filtered_tasks:
      print(f"{task[2]} - {task[0]} - {task[1]}")
      
    input("\nPress Enter to continue...\n")
    os.system('clear')

while True:
  print("\n1. Add Task")
  print("2. Remove Task")
  print("3. View Task")
  print("4. Edit Task")
  print("5. filter Task\n")

  menu = input(">" ).lower().strip()
  if menu == "1":
    add_task()
  elif menu == "2":
    remove_task()
  elif menu == "3":
    view_task()
  elif menu == "4":
    edit_task()
  elif menu == "5":
    filter_task()
  else:
    print("Invalid Option")
    time.sleep(1.5)
    os.system('clear')