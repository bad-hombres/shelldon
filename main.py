import cmd, sys, importlib, os, glob

class MainLoop(cmd.Cmd):
    def load_modules(self):
        self.loaded_commands = {}
        path = os.path.join(self.app_dir, "commands")
        for x in glob.glob(os.path.join(path, "*.py")):
            module_name = os.path.basename(x).replace(".py", "")
            module = importlib.import_module("commands.{}".format(module_name), "commands")
            self.loaded_commands[module.COMMAND_PREFIX] = module.Command(self)
            self.loaded_commands[module.COMMAND_PREFIX].setup(module_name, self.app_dir)

            help_name = f"help_{module.COMMAND_PREFIX}"
            complete_name = f"complete_{module.COMMAND_PREFIX}"
            help_code = f"""def {help_name}(): print(\"\"\"{module.HELP_TEXT}\"\"\")"""
            complete_code = f"""def {complete_name}(text, line, begin, end): return [x.replace(\"do_\", \"\") for x in {self.loaded_commands[module.COMMAND_PREFIX].get_names()} if x.startswith(\"do_\" + text)] """
            tmp = {}
            exec(help_code, tmp)
            exec(complete_code, tmp)
            setattr(self, help_name, tmp[help_name])
            setattr(self, complete_name, tmp[complete_name])

    def __init__(self, app_name, app_dir = None):
        cmd.Cmd.__init__(self)
        self.app_name = app_name
        self.prompt = f"[{self.app_name}]> "
        self.app_dir = app_dir
        if not app_dir:
            self.app_dir = os.path.dirname(sys.argv[0])

        self.app_dir = os.path.abspath(self.app_dir)
        self.load_modules()

    def do_reload(self, line):
        """Command that reloads all the modules"""
        self.load_modules()

    def completenames(self, text, *ignored):
        names = [x for x in self.loaded_commands.keys() if x.startswith(text)]
        return super().completenames(text, *ignored) + names

    def default(self, line):
        module_name, *args = line.split(" ")
        module = self.loaded_commands.get(module_name, None)
        if module:
            module.onecmd(" ".join(args))
        else:
            print("unkown command")

    def emptyline(self):
        return 0

    def do_interact(self, line):
        if len(line) == 9:
            print("specify module to interact with")

        module_name = line.split(" ")[0]
        module = self.loaded_commands[module_name]
        module.cmdloop()

    def complete_interact(self, text, line, begin, end):
        return [x for x in self.loaded_commands.keys() if x.startswith(text)]

    def completedefault(self, text, line, begin, end):
        return []

    def do_exit(self, line):
        return True

def main():
    loop = MainLoop("example_shell")
    loop.cmdloop()

if __name__ == "__main__":
    main()
