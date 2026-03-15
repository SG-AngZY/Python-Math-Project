import numpy as np


def dot_product(A, B):
    """Return the dot product of two vectors."""
    return np.dot(A, B)

def cross_product(A, B):
    """Return the cross product of two 3D vectors."""
    if len(A) != 3 or len(B) != 3:
        raise ValueError("Cross product is only defined for 3D vectors.")
    return np.cross(A, B)

def vector_input(name):
    """Prompts the user to input a vector and returns it as a NumPy array."""
    values = input(f"Enter the components of {name} (separated by spaces): ")
    return np.array(list(map(float, values.split())))

def vector_menu():
    """Runs the interactive vector calculator menu."""
    print("=== Universal Math App: Vector Module ===")
    log = []

    while True:
        print("\nChoose an operation:")
        print("1. Dot Product (or type 'dot')")
        print("2. Cross Product (or type 'cross')")
        print("3. View Log (or type 'log')")
        print("4. Clear Log (or type 'clear')")
        print("5. Exit (or type 'exit')")

        choice = input("Enter your choice: ").strip().lower()

        # Normalize commands
        if choice in ['1', 'dot']:
            choice = '1'
        elif choice in ['2', 'cross']:
            choice = '2'
        elif choice in ['3', 'log']:
            choice = '3'
        elif choice in ['4', 'clear']:
            choice = '4'
        elif choice in ['5', 'exit', 'quit']:
            choice = '5'
        else:
            print("❌ Invalid choice, please try again.")
            continue

        if choice == '5':
            print("Returning to main menu... 👋")
            break

        elif choice == '3':
            if log:
                print("\n=== Session Log ===")
                for i, entry in enumerate(log, start=1):
                    print(f"{i}. {entry}")
            else:
                print("📝 Log is empty.")
            continue

        elif choice == '4':
            if log:
                confirm = input("Are you sure you want to clear the log? (y/n): ").lower()
                if confirm == 'y':
                    log.clear()
                    print("✅ Log cleared successfully.")
                else:
                    print("❎ Log not cleared.")
            else:
                print("📝 Log is already empty.")
            continue

        # Only for math operations
        A = vector_input("Vector A")
        B = vector_input("Vector B")

        if choice == '1':
            result = np.dot(A, B)
            print(f"Dot Product: {result}")
            log.append(f"Dot Product | A={A}, B={B}, Result={result}")

        elif choice == '2':
            if len(A) == 3 and len(B) == 3:
                result = np.cross(A, B)
                print(f"Cross Product: {result}")
                log.append(f"Cross Product | A={A}, B={B}, Result={result}")
            else:
                print("⚠️ Cross product only works for 3D vectors.")
                
if __name__ == "__main__":
    vector_menu()
