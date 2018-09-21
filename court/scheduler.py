import random
import math
import mesa

from collections import defaultdict
from mesa.time import BaseScheduler


class CourtScheduler(BaseScheduler):
    """ Simulates activation of Jurors and Randomly Selected Tokens
        Assumes that model keeps track of dispute_level when calling step
        Assumes that model calls reset

    """
    def __init__(self, model, base_dispute_size):
        super().__init__(model)
        self.base_dispute_size = base_dispute_size
        self.jurors = defaultdict(dict)
        self.tokens = defaultdict(dict)
        self.juror_keys = []
        self.token_keys = []
        self.token_index = 0

    def add(self, agent):
        '''
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        '''
        agent_class = type(agent).__name__
        if agent_class == 'Juror':
            self.jurors[agent.unique_id] = agent
        elif agent_class == 'Token':
            self.tokens[agent.unique_id] = agent

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''
        agent_class = type(agent).__name__
        if agent_class == 'Juror':
            del self.jurors[agent.unique_id]
        elif agent_class == 'Token':
            del self.tokens[agent.unique_id]

    def step(self):
        '''
            If initial dispute level activates all jurors.
            Randomly selects and activates tokens based on dispute level.
        '''

        if self.model.dispute_level == 1:
            self.token_index = 0
            self.juror_keys = list(self.jurors.keys())
            random.shuffle(self.juror_keys)
            for juror_key in self.juror_keys:
                self.jurors[juror_key].step()
            self.token_keys = list(self.tokens.keys())
            random.shuffle(self.token_keys)
            for token_key in self.token_keys:
                if self.token_index <= self.base_dispute_size:
                    self.token_index += 1
                    self.tokens[token_key].step()
                else:
                    break
        else:
            for token_key in self.token_keys[self.token_index:]:
                if self.token_index <= self.base_dispute_size * math.pow(2,self.model.dispute_level):
                    self.token_index += 1
                    self.tokens[token_key].step()
                else:
                    break

        self.steps += 1
        self.time += 1

    def reward(self):
        """ Redistributes tokens to jurors based on the outcome of the dispute and cleans up agent queue """
        for juror_key in self.juror_keys:
            if self.jurors[juror_key].votes > 0:
                self.jurors[juror_key].process_reward()
        for token_key in self.token_keys:
            self.remove(self.tokens[token_key])

    def get_type_count(self, class_name):
        '''
        Returns the current number of agents of certain type in the queue.
        '''
        if class_name == 'Juror':
            return len(self.jurors.values())
        elif class_name == 'Token':
            return len(self.tokens.values())
