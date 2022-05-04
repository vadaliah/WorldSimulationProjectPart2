import math

from GlobalConstants import *


class Country:
    def __init__(self, name, self_flag):
        self._name = name
        self._self_flag = self_flag
        self._resources = {}
        self._state_quality = 0
        self._undiscounted_reward = 0
        self._discounted_reward = 0
        self._probability_succeds = 0
        self._expected_utility = 0
        self._score=0

    def __getitem__(self, items):
        print(type(items), items)

    def verify_required_resources(self, action):
        for key, value in action.input_resources.items():
            if value > 0 and value > self._resources[key]:
                print(f"Country: {self['Country']} Resource :{key} failed resource check")
                return False
        return True

    def apply_template(self, action):
        """
        Function to apply action template on a country object
        Country Resources are reduced as per Template Input Resource definition
        Country Resources are added as per Template Out Resource definition
        Additional Country Resources are created for non-existing Template Out resources
        :param action:
        :return:
        """
        country_successor = Country(self._name, self._self_flag)
        country_successor._resources =self._resources

        for key, value in action.input_resources.items():
            if value > 0:
                country_successor._resources[key] -=  value
        for key, value in action.output_resources.items():
            if value > 0:
                country_successor._resources[key] +=  value
        return country_successor

    def calculate_state_quality(self, resource_weights):
        """
            # Function to calculate Node State Quality
            :param
            Input: Node object
            Input: resourceweights: Map object containing Resource Weight definition
            # Part1 State quality function uses static Weights associated per resource type
            # For Part , intend to enhance weights using country specific methodology
        """
        state_quality = 0
        [state_quality := state_quality+ amount * resource_weights[resource] for resource, amount in self._resources.items() if resource_weights.get(resource) is not None ]
        self._state_quality = state_quality
        return self._state_quality

    def get_state_quality(self):
        return self._state_quality

    def calculate_undiscounted_reward(self, root_node):
        """
        # From the requirements, this function implements the following equation:
        # R(c_i, s_j) = Q_end(c_i, s_j) – Q_start(c_i, s_j) to a country c_i of a schedule s_j.
        :param :
        :undiscounted_reward: state_quality(child) - state_quality(parent)
        """
        root_country = [country for country in root_node.world if country._name == self._name ]

        self._undiscounted_reward = (self._state_quality - root_country[0]._state_quality if root_country[0] is not None else 0)
        return self._undiscounted_reward

    def get_undiscounted_reward(self):
        """
               # From the requirements, this function implements the following equation:
               # R(c_i, s_j) = Q_end(c_i, s_j) – Q_start(c_i, s_j) to a country c_i of a schedule s_j.
               :param :
               :return: undiscounted_reward= state_quality(child) - state_quality(parent)
        """
        return self._undiscounted_reward

    def calculate_discounted_reward(self, root_node, depth):
        """
        Calculate discounted_reward using following equation:
        # DR(c_i, s_j) = gamma^N * (Q_end(c_i, s_j) – Q_start(c_i, s_j)), where 0 <= gamma < 1.
        :return: (Gamma ** depth) * country.calculate_undiscounted_reward()
        """
        root_country = [country for country in root_node.world if country._name == self._name ]

        self._discounted_reward = (gamma ** depth)*self._state_quality - root_country[0]._state_quality if root_country[0] is not None else 0
        return self._discounted_reward

    def get_discounted_reward(self):
        """
        :return: (Gamma ** depth) * country.calculate_undiscounted_reward()
        """
        return self._discounted_reward

    def calculate_schedule_probability(self):
        """
        Calculates Country Schedule Probability score:L / 1 + math.e ** (-K * (x - X_0))

        :return:
        """
        l = 1
        x = self.get_discounted_reward()
        score = l / 1 + math.e ** (-k * (x - x_0))
        self._score = score
        return self._score

    def get_schedule_probability(self):
        """
        :return: Country Schedule probability score
        """
        return self._score

    def calculate_expected_utility(self):
        """
         # calculate_expected_utility function implements the following:
        # EU(c_i, s_j) = (P(s_j) * DR(c_i, s_j)) + ((1-P(s_j)) * C), where c_i = self
        :return:
        """

        p = self.get_schedule_probability()
        dr = self.get_discounted_reward()
        self._expected_utility = (p * dr) + ((1 - p) * c)
        return self._expected_utility

    def get_expected_utility(self):
        return self._expected_utility

    def get(self, country_key):
        pass
