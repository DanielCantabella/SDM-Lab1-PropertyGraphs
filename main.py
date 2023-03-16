from functions.util import *
from functions.partA_2_CantabellaZarate import partA2
from functions.partA_3_CantabellaZarate import partA3
from functions.partB_CantabellaZarate import partB
from functions.partC_CantabellaZarate import partC
from functions.partD_CantabellaZarate import partD

if __name__ == '__main__':
    while True:
        printLine("=", 70)
        print("Property Graphs Lab")
        printLine("=", 70)
        print('Select the task you want to execute: ')
        print("1. Task A2 - Graph loading")
        print("2. Task A3 - Graph evolving")
        print("3. Task B - Query execution")
        print("4. Task C - Recommender")
        print("5. Task D - Algorithm execution")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            partA2()
        elif choice == "2":
            partA3()
        elif choice == "3":
            partB()
        elif choice == "4":
            partC()
        elif choice == "5":
            partD()
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 5.")
        printLine("=", 70)
        input("Press enter to return to the menu...")
