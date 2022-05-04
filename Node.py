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
    def parent(self, value):
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

    def generate_successor(self, frontier, schedule_queue, depth, actions, root_node, resource_weights, my_country):
        """
            Function that generates applies Action on Each Countries within Node.World to generate Successor Nodes
        """
        for action in actions:
            world_successor = []
            for country in self.world:
                if country.verify_required_resources(action):  # Verify Country has adequate resources to apply Action template
                    print(f"Applying Template:{action.TemplateName} for county:{country._name}")
                    country_successor = country.apply_template(action)
                else:
                    print(
                        f"county:{country['Country']} does not have sufficient resources for:{action['TemplateName']}")
                    continue
                country_successor.calculate_state_quality(resource_weights)
                country_successor.calculate_undiscounted_reward(root_node)
                country_successor.calculate_discounted_reward(root_node, depth)
                country_successor.calculate_schedule_probability()
                country_successor.calculate_expected_utility()
                world_successor.append(country_successor)
            child = Node()
            child.parent = self
            child.world = world_successor
            child.actions = action
            child.get_state_quality(my_country)
            child.get_undiscounted_reward(my_country)
            child.get_schedule_probability(my_country)
            schedule_str = ':'.join(
                ['Depth', str(depth), 'State_Quality', str(round(child.get_state_quality(my_country))), 'Operation',
                 child.get_state_operator()])
            #
            parent_str = '--'.join('{} : {}'.format(key, value) for key, value in country._resources.items())
            child_str = '--'.join('{} : {}'.format(key, value) for key, value in country_successor._resources.items())
            schedule_str += ':'.join([' Parent', parent_str, ' Child', child_str])
            schedule_queue.put(schedule_str, child)
            schedule_queue.put(schedule_str, child)
            frontier.put((-1 * child.get_state_quality(my_country), child))

    def get_state_operator(self):
        return ':'.join([self._actions.Operation, self._actions.TemplateName])

    def get_state_quality(self, my_country_name):
        my_country = [country for country in self.world if country._name == my_country_name]
        return my_country[0].get_state_quality() if my_country[0] is not None else 0

    def get_undiscounted_reward(self, my_country_name):
        """
           # From the requirements, this function implements the following equation:
           # R(c_i, s_j) = Q_end(c_i, s_j) – Q_start(c_i, s_j) to a country c_i of a schedule s_j.
           :param :
           :return: state_quality(node) - state_quality(start)
           """
        my_country = [country for country in self.world if country._name == my_country_name]
        return my_country[0].get_undiscounted_reward() if my_country[0] is not None else 0
        # for country in self.world:
        #     return country.get_undiscounted_reward() if country._name == my_country else 0

    def get_discounted_reward(self, my_country_name):
        """
               Calculate discounted_reward using following equation:
               # DR(c_i, s_j) = gamma^N * (Q_end(c_i, s_j) – Q_start(c_i, s_j)), where 0 <= gamma < 1.
               :return: (Gamma ** count) * node.calculate_undiscounted_reward()
               """
        my_country = [country for country in self.world if country._name == my_country_name]
        return my_country[0].get_discounted_reward() if my_country[0] is not None else 0

    def get_schedule_probability(self, my_country_name):
        my_country = [country for country in self.world if country._name == my_country_name]
        return my_country[0].get_schedule_probability() if my_country[0] is not None else 0

    def get_expected_utility(self, my_country_name):
        """
           # calculate_expected_utility function implements the following:
          # EU(c_i, s_j) = (P(s_j) * DR(c_i, s_j)) + ((1-P(s_j)) * C), where c_i = self
          :return:
          """
        my_country = [country for country in self.world if country._name == my_country_name]
        return my_country[0].get_expected_utility() if my_country[0] is not None else 0

