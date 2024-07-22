from typing import Callable, Any


class CommandListener():
    def __init__(self) -> None:
        self._running = False
        self._commands: dict[str, Callable[[str | None], Any]] = {}

        @self.register_command("help", "displays existing commands")
        def help_command(args: str):
            print("The list of available commands:")
            for cmd in self.get_commands():
                func, help = self._commands[cmd]
                print("    %s" % cmd, "- %s " % help if help else "")
            print()


    def register_command(self, command: str, help: str | None = None):
        """A decorator to register a new command, binding the
        decorated function to the command's execution.

        Spaces will be trimmed, e.g., "My Amazing Command" will
        be registred as "MyAmazingCommand".

        Case insensetive, e.g., "MyAmazingCommand" and "myamazingcommand"
        are the same commadn.
        
        `help` is optional and is displayed shown by using
        command 'help'."""
        def wrapper(func: Callable[[str | None], Any]):
            cmd = str().join(command.split())
            self._commands.update( {cmd.lower(): [func, help]} )
            return func
        return wrapper
        
    def get_commands(self) -> list[str]:
        """Returns the registred commands"""
        return sorted(self._commands.keys())
    
    def run(self) -> None:
        self._running = True
        """Runs the main loop of the command listener
        that will react on the command line's input."""
        try:
            while self._running:
                print("Enter command > ", end="")
                i = input().split(maxsplit = 1)
                if i:
                    try:
                        func, _ = self._commands[i[0].lower()]
                        func(''.join(i[1:]))
                    except KeyError:
                        print(f"No {i[0]} command found")
        except KeyboardInterrupt:
            print("The program is terminated by the user.")

    def stop(self) -> None:
        self._running = False
