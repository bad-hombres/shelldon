import cmd, shlex, inspect, os, json
from docopt import docopt, DocoptExit

class CommandBase(cmd.Cmd):
    def __init__(self, parent):
        cmd.Cmd.__init__(self)
        self.parent = parent
        self.options = {}
        self.allowed_options = []

    def setup_allowed_options(self): pass 

    def setup(self, module_name, app_dir):
        print(f"[+] {module_name}: loaded.")
        self.allowed_options = []
        self.options = {}
        self.app_dir = app_dir

        self.module_name = module_name
        self.setup_allowed_options()
        self.config_path = os.path.join(self.app_dir, "config", f"{module_name}.json")
        if os.path.isfile(self.config_path):
            data = json.load(open(self.config_path))
            if "options" in data: 
                self.options = data["options"] 
        else:
            self.config_path = None

    def emptyline(self):
        return 0

    def complete(self, text, state):
        completions = super().complete(text, state)
        
        if completions == None: 
            completions = self.parent.complete(text, state)

        return completions

    def completedefault(self, text, line, begin, end):
        return []

    def get_args(self, line):
        params = shlex.split(line)        
        doc = getattr(self, inspect.stack()[1][3]).__doc__

        try:
            args = docopt(doc, argv=params)
            return args
        except DocoptExit as e:
            print(doc) 
        except SystemExit as s:
            pass

    def add_option(self, option, value):
        self.options[option] = value

    def do_set(self, line):
        """Usage: set OPTION VALUE"""

        args = self.get_args(line)
        if args:
            if args["OPTION"] in self.allowed_options:
                self.add_option(args["OPTION"], args["VALUE"]) 
                self.set_prompt()
            else:
                print("[!] Option not allowd")

    def complete_set(self, line, text, *ignored):
        if len(line) == 0:
            return self.allowed_options
        else:
            return [x for x in self.allowed_options if x.startswith(line)]

    def help_set(self):
        print("Usage:")
        for o in self.allowed_options:
            print(f"\t set {o} VALUE")

    def do_status(self, line):
        print("Options:")
        status = self.get_status()

        for k,v in status["options"].items():
            print(f"\t{k} = {v}")

        for k, v in status["extra"].items():
            print(f"{k.capitalize()}: {v}")

    def get_status(self):
        return {"options": self.options, "extra": {"config": self.config_path, "status": "OK"}}

    def do_revert_config(self, line):
        self.setup(self.module_name, self.app_dir)

    def default(self, line):
        return self.parent.onecmd(line)

    def additional_prompt(self):
        return self.module_name

    def set_prompt(self):
        self.prompt = "[{}][{}]> ".format(self.parent.app_name, self.additional_prompt())

    def preloop(self):
        self.set_prompt()
