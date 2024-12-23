class Print:
    COLORS = {
        "RED":      "\033[91m",
        "GREEN":    "\033[92m",
        "YELLOW":   "\033[93m",
        "BLUE":     "\033[96m",
        "WHITE":    "\033[97m",
        "RESET":    "\033[0m",
    }

    LABELS = {
        "INFO":     "INFO",
        "ERROR":    "FAIL",
        "SUCCESS":  " OK ",
        "DEBUG":    "DEBG",
    }

    @staticmethod
    def log(message, level="info"):
        """basic logger method"""
        color_mapping = {
            "INFO": Print.COLORS["YELLOW"],
            "ERROR": Print.COLORS["RED"],
            "SUCCESS": Print.COLORS["GREEN"],
            "DEBUG": Print.COLORS["BLUE"],
        }
        color = color_mapping.get(level, Print.COLORS["WHITE"])
        label = Print.LABELS.get(level, "LOG")

        label_section = f"[ {color}{label}{Print.COLORS['RESET']} ]"

        print(f"{label_section} {message}")

    @staticmethod
    def info(message):
        Print.log(message, level="INFO")

    @staticmethod
    def error(message):
        Print.log(message, level="ERROR")

    @staticmethod
    def success(message):
        Print.log(message, level="SUCCESS")

    @staticmethod
    def debug(message):
        Print.log(message, level="DEBUG")

    @staticmethod
    def input(prompt):
        """Prompt user input with colored text."""
        colored_prompt = f"{Print.COLORS['WHITE']}{prompt}{Print.COLORS['RESET']}"
        return input(colored_prompt).strip()

if __name__ == "__main__":
    Print.info("Info message")
    Print.success("Successful message")
    Print.error("Error message")
    Print.debug("Debug message")
    user_input = Print.input("Input: ")
    Print.info(f"Inputed: {user_input}")