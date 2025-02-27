from dotenv import load_dotenv
load_dotenv()
from search_controller import SearchController
from sql_connection import SqlConnection


def list_methods(cls):
    methods = [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("__")]
    return methods

def entry_point():
    search_controller = SearchController()
    methods = list_methods(SearchController)

    while not search_controller.exit_flag:
        print("Available options:")
        for index, method_name in enumerate(methods):
            print(f"{index}. {method_name}")

        try:
            choice = int(input("Enter the number of the method you want to run: "))
            if 0 <= choice < len(methods):
                method_name = methods[choice]
                method = getattr(search_controller, method_name)
                method()
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def tear_down():
    SqlConnection().tear_down()

if __name__ == "__main__":
    try:
        entry_point()
    finally:
        tear_down()
