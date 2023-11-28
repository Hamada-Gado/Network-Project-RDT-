class Colors:
    ENDC = "\033[0m"

    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def cprint(colors, *args, **kwargs):
        print(colors, end="")
        print(*args, end="")
        print(Colors.ENDC, end="")
        print(**kwargs)

    @staticmethod
    def print_sender(action, *args, **kwargs):
        Colors.cprint(Colors.OKBLUE + Colors.BOLD, "Sender:", end=" ")
        Colors.cprint(Colors.OKBLUE + Colors.UNDERLINE, action, end=" ")
        print(*args, **kwargs)

    @staticmethod
    def print_reciver(action, *args, **kwargs):
        Colors.cprint(Colors.OKGREEN + Colors.BOLD, "Reciver:", end=" ")
        Colors.cprint(Colors.OKGREEN + Colors.UNDERLINE, action, end=" ")
        print(*args, **kwargs)

    @staticmethod
    def print_network(action, *args, **kwargs):
        Colors.cprint(Colors.FAIL + Colors.BOLD, "Network_layer:", end=" ")
        Colors.cprint(Colors.FAIL + Colors.UNDERLINE, action, end=" ")
        print(Colors.FAIL, *args, **kwargs)
