from rich.console import Console
from ServerMonitoring import menu
from ServerMonitoring import dashboard

console = Console()

def main():
    while True:
        menu.show_menu()
        choice = console.input("Enter your choice(0-3): ")
        
        if choice == "1":
            dashboard.run_live_dashboard()
            console.input("\nPress Enter to return to menu...")
        elif choice == "2":
            menu.run_stress_test()
            console.input("\nPress Enter to return to menu...")
        elif choice == "3":
            menu.view_alert_history()
            console.input("\nPress Enter to return to menu...")
        elif choice == "0":
            menu.stop_stress_if_running()
            console.print("\nGoodbye!\n")
            break
        else:
            console.print("\nInvalid choice")
            console.input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        menu.stop_stress_if_running()
        console.print("\n\nInterrupted\n")
    except Exception as e:
        menu.stop_stress_if_running()
        console.print(f"\nError: {e}\n")
