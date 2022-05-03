import math
from copy import deepcopy

from Country import Country
from GlobalConstants import *


class Node:
    def __init__(self):
        self._parent = None
        self._world = None
        self._actions = None
        self._score = 0
        self._children = []

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self,value):
        self._parent = value

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        if value is None:
            raise ValueError("value can't be None")
        self._world = value

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, value):
        self._actions = value


    def __str__(self):
        # resource_str= '-'.join(self.resources)
        return f"children_cnt: {len(self.children)}"

    def get_first_child(self):
        """
        :return: Return First Child with max state_quality
        """
        node = self
        if node._children:
            for i in len(node._children):
                child = node._childeren[i]
                if child.country == 1:
                    return child
        else:
            return None

    def calculate_schedule_probability(self):
        """
        :return: Schedule Probability sco:L / 1 + math.e ** (-K * (x - X_0))
        """
        node = self
        l = 1
        x = node.calculate_discounted_reward()
        score = l / 1 + math.e ** (-k * (x - x_0))
        self.score = score
        return score

    def calculate_expected_utility(self):
        """
         # calculate_expected_utility function implements the following:
        # EU(c_i, s_j) = (P(s_j) * DR(c_i, s_j)) + ((1-P(s_j)) * C), where c_i = self
        :return:
        """
        node = self
        p = node.calculate_schedule_probability()
        dr = node.calculate_discounted_reward()
        return (p * dr) + ((1 - p) * c)

    def get_children_count(self):
        node = self
        if node._children is None:
            return 0
        return 1 + len(node._children)



    def get_probability_score(self):
        """
        Probability_score Getter
        :return: node.score
        """
        node = self
        if node is None:
            return 0
        return node.score

    def calculate_undiscounted_reward(self):
        """
        # From the requirements, this function implements the following equation:
        # R(c_i, s_j) = Q_end(c_i, s_j) – Q_start(c_i, s_j) to a country c_i of a schedule s_j.
        :param :
        :return: state_quality(node) - state_quality(start)
        """

        sq1 = (self.get_first_child()).get_state_quality() if self.children else 0

        return self.get_state_quality() - sq1

    def calculate_discounted_reward(self):
        """
        Calculate discounted_reward using following equation:
        # DR(c_i, s_j) = gamma^N * (Q_end(c_i, s_j) – Q_start(c_i, s_j)), where 0 <= gamma < 1.
        :return: (Gamma ** count) * node.calculate_undiscounted_reward()
        """
        count = self.get_children_count()
        return (gamma ** count) * self.calculate_undiscounted_reward()

    def generate_successor(self,  frontier, schedule_queue, depth, actions,root_node,resource_weights):
        """
            Function that generates applies Action on Each Countries within Node.World to generate Successor Nodes
        """
        self.children = []
        for action in actions:
            world_successor = []
            for country in self.world:
                if country.verify_required_resources(action):  # Verify Country has adequate resources to apply Action template
                    print(f"Applying Template:{action.TemplateName } for county:{country._name}")
                    country_successor = country.apply_template(action)
                else:
                    print(
                        f"county:{country['Country']} does not have sufficient resources for:{action['TemplateName']}")
                country_successor.calculate_state_quality(resource_weights)
                country_successor.calculate_undiscounted_reward(root_node)
                country_successor.calculate_discounted_reward(root_node,depth)
                country_successor.calculate_schedule_probability()
                world_successor.append(country_successor)
            child = Node();
            child.parent=self
            child.world=world_successor
            child.actions=action
            # child.calculate_state_quality(resource_weights)
            # child.calculate_undiscounted_reward()
            # child.calculate_schedule_probability()
            # schedule_str = ':'.join(
            #     ['Depth', str(depth), 'State_Quality', str(round(child.get_state_quality())), 'Template',
            #      action['TemplateName']])
            #
            parent_str = '--'.join('{} : {}'.format(key, value) for key, value in country.items())
            child_str = '--'.join('{} : {}'.format(key, value) for key, value in country_successor.items())
            # schedule_str += ':'.join([' Parent', parent_str, ' Child', child_str])
            #    schedule_str+= ':'.join()
            # schedule_queue.put(schedule_str, child)
            # schedule_queue.put(schedule_str, child)
            frontier.put((-1, child))
            # frontier.put((-1 * child.state_quality, child))


    def calculate_state_quality(self, resource_weights):
        """
            # Function to calculate Node State Quality
            :param
            Input: Node object
            Input: resourceweights: Map object containing Resource Weight definition
            # Part1 State quality function uses static Weights associated per resource type
            # For Part , intend to enhance weights using country specific methodology
        """
        state_quality_map = {}
        for country in self.world:
            state_quality_map[country] = country.calculate_state_quality(resource_weights)

    def get_state_quality(self,my_country):
        for country in self.world:
            if (country.name == my_country):
                return country.state_quality

