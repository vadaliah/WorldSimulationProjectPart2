import math
from queue import PriorityQueue

from GlobalConstants import *
from Node import Node
from Utils import load_initial_state, load_resource_weights, load_templates


# from the requirements, uses the logistic function:
# https://en.wikipedia.org/wiki/Logistic_function
def calculate_schedule_probability(node):
    L = 1
    K = 1
    x = node.calculate_discounted_reward()

    return L / 1 + math.e ** (-K * (x - x_0))




def my_country_scheduler(my_country_name, resource_weight_filename, country_resources_filename,
                         action_template_filename,
                         output_schedule_filename, num_output_schedules, depth_bound, frontier_max_size):
    """
    u
    :param my_country_name:  My Country
    :param resource_weight_filename: Input CSV file for Resource Weights
    :param country_resources_filename:  Input CSV File for World Countries Resource definition
    :param action_template_filename: Input CVS file for Templates
    :param output_schedule_filename: Output CSV file for generated Schedules
    :param num_output_schedules:  Threshold for Output_schedules
    :param depth_bound:  Threshold for Schedule Depth
    :param frontier_max_size: Threshold for Frontier size
    :return:
    """

    resource_weights = load_resource_weights(resource_weight_filename)
    world = load_initial_state(country_resources_filename,resource_weights)
    actions = load_templates(action_template_filename)
    frontier = PriorityQueue()
    schedule_queue = PriorityQueue()
    current_depth = 0
    root_node = Node()
    root_node.world=world
    # score = root_node.calculate_schedule_probability()
    score = 0
    frontier.put((-1 * score, root_node))

    # schedule_str = ':'.join(
    #     ['Depth', str(current_depth), 'Probability_score', str(root_node.get_probability_score()), 'ROOT Node'])le+
    schedule_str = ''
    schedule_queue.put(schedule_str, root_node)

    while not frontier.empty() and current_depth <= depth_bound:
        node = frontier.get()[1]
        current_depth += 1
        node.generate_successor(frontier, schedule_queue, current_depth, actions,root_node,resource_weights)

def main():
    my_country_scheduler('Atlantis', r'resourcedefination.csv',
                         r'initialcountry.csv',
                         r'TransformTemplates.csv',
                         r'Schedule_results.txt', 10, 2, 500)


if __name__ == "__main__":
    main()
