import command

COMMAND_PREFIX = "some_module"
HELP_TEXT = """Some Module:
This submodule helps blah blah
"""

class Command(command.CommandBase):
    def setup_allowed_options(self):
        self.allowed_options.append("HOST")
        self.allowed_options.append("API_TOKEN")

    def do_mike(self, line):
        """Usage: 
    mike INPUT
    mike (-h|--help)"""

        args = self.get_args(line)
        if args:
            print(f"Hello {args['INPUT']}")

    def additional_prompt(self):
        prompt = super().additional_prompt()
        if "HOST" in self.options:
            return f"{prompt} : {self.options['HOST']}"
        else:
            return prompt
