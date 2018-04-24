#! python3
# Created: 4/22/18
import sqlite3
import pandas as pd


def check_for_table():
    try:
        CUR.execute("SELECT * FROM Dogtags")
    except sqlite3.OperationalError:
        create_table()


def create_table():
    """Creates table for dogtags"""
    CUR.execute("""CREATE TABLE Dogtags(
                    Name TEXT,
                    Level INTEGER,
                    Faction TEXT,
                    Cause_of_death TEXT,
                    Time TEXT)""")


def clear_table():
    user_choice = input("Are you sure? This will wipe any table that exists.(Y/N)").upper()
    if user_choice == 'Y':
        CUR.execute("DROP TABLE IF EXISTS Dogtags")
        create_table()
        print("Table created successfully.")


def insert_data(dt_info):
    """Insert data into table
        ARGS:
             dt_info"""
    CUR.execute("""INSERT INTO Dogtags (Name, Level, Faction, Cause_of_death, Time)
                   VALUES (?, ? ,? ,? ,?)""", (*dt_info,))
    CONN.commit()


def dogtag_loop():
    """Asks user number of dogtags to be entered and runs loop."""
    valid = False
    while not valid:
        try:
            num_of_dt = int(input("How many number of dogtags would you like to enter? "))
            for i in range(num_of_dt):
                print("Player {}: ".format(i + 1))
                dt_info = get_info()
                insert_data(dt_info)
            valid = True
        except ValueError:
            print("Enter a positive number")


def get_info():
    """Get info for dogtag (Name, Level, Faction, Cuase of death, time of death"""
    name = get_name()
    level = get_level()
    faction = get_faction()
    cause_of_death = input("Input cause of death: ")
    time = input("Enter time of death(HH:mm(AM/PM) - MM/dd/YY): ")
    return (name, level, faction, cause_of_death, time)


def get_name():
    """Get username of dogtag"""
    valid = False
    while not valid:
        name = input("Enter Player's name: ")
        if 0 < len(name) < 16:
            valid = True
    return name


def get_level():
    """Get player level"""
    level = 0
    while not 0 < level < 60:
        level = int(input("Enter Player's level(1-59): "))
        if not 0 < level < 60:
            print("Enter a level between 1 and 59")
    return level


def get_faction():
    """Asks user for player's faction"""
    user_choice = 0
    while user_choice not in [1, 2]:
        user_choice = int(input("Choose players faction:\n1) USEC\n2) Bear\nChoice: "))
        if user_choice == 1:
            faction = "USEC"
        if user_choice == 2:
            faction = "Bear"
        if user_choice not in [1, 2]:
            print("Error: Enter a valid choice\n")
    return faction


def print_table():
    """Prints SQL table"""
    CUR.execute("SELECT COUNT(Name) FROM Dogtags")
    if CUR.fetchone()[0] == 0:
        print("Table empty, no data available.")
        return None
    print(pd.read_sql_query("SELECT * FROM Dogtags", CONN))


def run_program():
    """Stars program and displays menu"""
    check_for_table()
    print("----------------\n"
          "EFT Kill Tracker\n"
          "----------------")
    user_choice = 1
    while user_choice != 0:
        try:
            user_choice = int(input("1)Display Table\n2)Enter new dogtag\n3)Clear data\n0)Exit Program\nChoice: "))
            if user_choice == 1:
                print_table()
                user_choice = input('\nContinue?(Y/N): ').upper()
                if user_choice != 'Y': break
            if user_choice == 2:
                dogtag_loop()
            if user_choice == 3:
                clear_table()
            if user_choice not in [1, 2, 3, 0]:
                raise ValueError
        except ValueError:
            print("Error: Enter a valid choice\n")
    print("Happy Raiding, Get those dogtags!")


if __name__ == '__main__':
    CONN = sqlite3.connect('DogTags.DB')
    CUR = CONN.cursor()
    run_program()
    CONN.close()
