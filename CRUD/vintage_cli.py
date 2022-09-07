import requests
import json


def check_server(cid=None):
    # returns True or False;
    # when invoked without arguments simply checks if server responds;
    # invoked with car ID checks if the ID is present in the database;
    if cid is not None:
        st = requests.head(f'http://localhost:5000/cars/{cid}').status_code
        return st == 200
    else:
        return requests.head('http://localhost:5000/cars').status_code == 200


def print_menu():
    # prints user menu - nothing else happens here;
    print('*' + '-'*30 + '*')
    print('|' + 'Vintage Car Database'.center(30) + '|')
    print('*' + '-'*30 + '*')
    print('M E N U')
    print('=======')
    print('1. List cars',
          '2. Add new car',
          '3. Delete car',
          '4. Update car',
          '0. Exit',
          sep='\n')


def read_user_choice():
    # reads user choice and checks if it's valid;
    # returns '0', '1', '2', '3' or '4'
    choice = input("Enter your choice (0..4): ")
    while choice not in ('0', '1', '2', '3', '4'):
        print('Invalid choice.')
        choice = input("Enter your choice (0..4): ")

    return choice


def print_header():
    # prints elegant cars table header;
    print('id'.ljust(10),
          'brand'.ljust(16),
          'model'.ljust(11),
          'production_year'.ljust(21),
          'convertible'.ljust(16),
          sep='| ', end='|\n')


def print_car(car):
    # prints one car's data in a way that fits the header;
    widths = (10, 16, 11, 21, 16)
    labels = ('id', 'brand', 'model', 'production_year', 'convertible')
    for i, w in zip(labels, widths):
        print(str(car[i]).ljust(w), end='| ')
    print()


def list_cars():
    # gets all cars' data from server and prints it;
    # if the database is empty prints diagnostic message instead;
    r = requests.get('http://localhost:5000/cars')
    if not r.json().get('cars'):
        print('Database is empty')
    else:
        print_header()
        for car in r.json().get('cars'):
            print_car(car)


def name_is_valid(name):
    # checks if name (brand or model) is valid;
    # valid name is non-empty string containing
    # digits, letters and spaces;
    # returns True or False;
    return name.isalnum()


def enter_id():
    # allows user to enter car's ID and checks if it's valid;
    # valid ID consists of digits only;
    # returns int or None (if user enters an empty line);
    entry = input('Car ID (empty string to exit): ')
    if entry.isdigit():
        return int(entry)


def enter_production_year():
    # allows user to enter car's production year and checks if it's valid;
    # valid production year is an int from range 1900..2000;
    # returns int or None  (if user enters an empty line);
    entry = input('Car production year (empty string to exit): ')
    try:
        return int(entry)
    except ValueError:
        pass


def enter_name(what):
    # allows user to enter car's name (brand or model)
    # and checks if it's valid;
    # uses name_is_valid() to check the entered name;
    # returns string or None  (if user enters an empty line);
    # argument describes which of two names
    # is entered currently ('brand' or 'model');
    entry = input(f'Car {what} (empty string to exit): ')
    if name_is_valid(entry):
        return entry


def enter_convertible():
    # allows user to enter Yes/No answer determining if the car is convertible;
    # returns True, False or None  (if user enters an empty line);
    choice = input('Is this car convertible? [y/n] (empty string to exit): ')
    if choice:
        return choice == 'y'


def delete_car():
    # asks user for car's ID and tries to delete it from database;
    entry = input('Car ID (empty string to exit): ')
    r = requests.delete(f'http://localhost:5000/cars/{entry}')
    if r.status_code == 200:
        print('Success!')
    else:
        print("Couldn't delete")


def input_car_data(with_id):
    # lets user enter car data;
    # argument determines if the car's ID is entered (True) or not (False);
    # returns None if user cancels the operation
    # or a dictionary of the following structure:
    # {'id': int, 'brand': str, 'model': str,
    # 'production_year': int, 'convertible': bool }
    dic = {}
    if with_id:
        id = enter_id()
        if id is None:
            return
        dic.update({'id': id})

    labels = ('brand', 'model', 'production_year', 'convertible')
    functions = (enter_name, enter_name,
                 enter_production_year, enter_convertible)
    for func, lab in zip(functions, labels):
        if lab in labels[:2]:
            aux = func(lab)
        else:
            aux = func()

        if aux is None:
            return
        dic[lab] = aux

    return dic


def add_car():
    # invokes input_car_data(True) to gather car's info and adds it to the database;
    data = input_car_data(True)
    if data is None:
        return
    if len(data) != 5:
        return
    requests.post('http://localhost:5000/cars',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(data))


def update_car():
    # invokes enter_id() to get car's ID if the ID is present in the database;
    # invokes input_car_data(False) to gather new car's info and updates the database;
    id = enter_id()
    data = input_car_data(False)
    data.update({'id': id})
    requests.put(f'http://localhost:5000/cars/{id}',
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps(data))


while True:
    if not check_server():
        print("Server is not responding - quitting!")
        exit(1)
    print_menu()
    choice = read_user_choice()
    if choice == '0':
        print("Bye!")
        exit(0)
    elif choice == '1':
        list_cars()
    elif choice == '2':
        add_car()
    elif choice == '3':
        delete_car()
    elif choice == '4':
        update_car()
