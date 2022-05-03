import json


class Action:
    def __init__(self, templatename, action):
        self.TemplateName = templatename
        self.Operation = action
        self.input_resources = {}
        self.output_resources = {}

    def __repr__(self):
        print (f"Action: {self.TemplateName}, input_resources: {json.dumps(self.input_resources)},output_resources: {json.dumps(self.output_resources)}")

    def add_input_resource(self, resource):
        self.input_resources.update(resource)

    def add_output_resource(self, resource):
        self.output_resources.update(resource)

    def __str__(self):
        # resource_str= '-'.join(self.resources)
        return f"Action: {self.TemplateName}"
