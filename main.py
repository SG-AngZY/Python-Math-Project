import os
import importlib

def get_available_modules():
    """Scans the 'modules' folder for all *_module.py files, relative to this script."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.join(base_dir, "modules")

    if not os.path.exists(module_dir):
        print("❌ Couldn't find the 'modules' folder. Make sure it's next to main.py.")
        return []

    module_files = [
        f[:-3] for f in os.listdir(module_dir)
        if f.endswith("_module.py") and not f.startswith("__")
    ]
    return module_files

def display_menu(modules):
    print("=== Universal Math App ===")
    print("\nAvailable Modules:")
    for i, mod in enumerate(modules, start=1):
        name = mod.replace("_module", "").capitalize()
        print(f"{i}. {name}")
    print(f"{len(modules) + 1}. Exit")

def main():
    while True:
        modules = get_available_modules()
        display_menu(modules)

        choice = input("\nEnter your choice: ").strip()
        if not choice.isdigit():
            print("❌ Please enter a number.")
            continue

        choice = int(choice)
        if choice == len(modules) + 1:
            print("Goodbye! 👋")
            break
        elif 1 <= choice <= len(modules):
            selected_module = modules[choice - 1]
            module_path = f"modules.{selected_module}"
            mod = importlib.import_module(module_path)

            # Run the module's menu if it exists
            if hasattr(mod, "vector_menu"):
                mod.vector_menu()
            elif hasattr(mod, "main_menu"):
                mod.main_menu()
            else:
                print(f"⚠️ {selected_module} has no main menu function.")
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
