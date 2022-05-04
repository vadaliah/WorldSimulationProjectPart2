import pandas as pd
import math
from IPython.core.display import Math

from Country import Country
from Action import Action


# Load World - Country Resources from Input file
def load_initial_state(country_resource_filename,resource_weights):
    """
    Function to load initial World Resource state from an input CSV file
    Panda dataframe is used to read CSV file for creating Country objects
    :param country_resource_filename:
    :return:
    """
    world = []
    df = pd.read_csv(country_resource_filename)
    df.fillna(0)
    for i in range(len(df)):
        resources = {}

        for j in range(len(df.columns)):
            if df.columns[j] == 'Country':
                country = Country(df.loc[i][j], False)
            else:
                resources[df.columns[j]] = df.loc[i][j]
        country._resources = resources
        country.calculate_state_quality(resource_weights)
        world.append(country)
    # df = pd.read_csv(initial_state_file_name)
    # country[df]
    return world


def load_resource_weights(resource_filename):
    """
    Function to populate resource-weights map of Resource Weights from an input CSV file
    :param resource_filename:
    :return: resource-weights
    """
    resourceweights = {}
    df = pd.read_csv(resource_filename)
    df.fillna(0)
    # print (df.columns.tolist())

    for i in range(len(df)):
        resourceweights[df.loc[i][0]] = df.loc[i][1]
    return resourceweights


def load_templates(template_filename):
    """
     Function to populate actions list  of Action Templates from an input CSV file
     Actions object consists of Action[Transform/Transfer], TemplateName, Input Resources : Resources required as Inputs
     and Output Resources: Resources generated as a Byproduct
     Panda DataFrame is used to Read CSV file and populate Action dictionary object
    :param template_filename:
    :return:
    """
    actions = []
    df = pd.read_csv(template_filename)
    df.fillna(0)
    for index, template in df.to_dict(orient="index").items():
        action = Action(template['TemplateName'],template['Action'])
        for key, value in template.items():
            resource = {}
            if key.startswith('IN_'):
                resource[key.removeprefix('IN_')] = value
                action.add_input_resource(resource)
            elif key.startswith('OUT_'):
                resource[key.removeprefix('OUT_')] = value
                action.add_output_resource(resource)
            else:
                continue
        actions.append(action)
    return actions


def print_schedule(schedulequeue, output_schedule_filename):
    """
    Function to print Schedules to an output file
    :param schedulequeue:
    :param output_schedule_filename:
    :return:
    """
    print(f"Printing Schedules to Output file: {output_schedule_filename} ")
    with open(output_schedule_filename, "w") as external_file:
        print("Printing Schedule", file=external_file)
        while not schedulequeue.empty():
            next_item = schedulequeue.get()
            print(next_item, file=external_file)
    external_file.close()


def logisticFunction(L, k, x0, x):
  return L / (1 + Math.pow(Math.E, -k * (x - x0)))



