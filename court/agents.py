import numpy as np
from mesa import Agent

class Token(Agent):
    """
    Tokens are controlled by Jurors. Jurors may control multiple tokens, but each token is selected for activation individually.
    """
    def __init__(self, unique_id, model, owner):
        super().__init__(unique_id, model)
        self.owner = owner

    def step(self):
        """
        When a token is activated it votes and increments the juror's active_tokens counter.
        """
        self.model.vote(self.owner.belief) # record vote in model
        self.owner.vote() # increment juror vote counter for redistribution calculation


class Juror(Agent):
    '''
    An idealized model for juror behavior.

    The agent follows the following logical behaviors:
        - Honest: Agent makes a noisy estimate of the models truth for a dispute and votes honestly
        - Consistent: Agent should not change belief even if activated by multiple tokens.
    '''
    def __init__(self, unique_id, model, sigma):
        super().__init__(unique_id, model)
        self.sigma = sigma
        self.tokens = self.model.token_count/self.model.juror_count
        self.belief = False
        self.votes = 0

    def vote(self):
        self.votes +=1

    def process_reward(self):
        '''If belief matches result the juror gains tokens, if belief does not match result the juror loses tokens'''
        if self.belief and self.model.result():
            self.tokens += (self.votes/self.model.true_votes) * self.model.false_votes * self.model.penalty_pct # win tokens
        elif not self.belief and not self.model.result():
            self.tokens += (self.votes/self.model.false_votes) * self.model.true_votes * self.model.penalty_pct # mechanism failure
        else:
            self.tokens -= self.votes * self.model.penalty_pct # lose tokens
        self.votes = 0 # reset votes after finishing dispute

    def get_belief(self):
        ''' Return true or false based on a noisy estimate of model's true_value '''
        self.raw_belief = np.random.normal(self.model.true_value, self.sigma)
        return self.model.true_value-self.model.threshold < self.raw_belief < self.model.true_value+self.model.threshold


    def step(self):
        ''' When activated a Juror Agent:
            1. Creates an interal estimation of the the model truth by calling get_belief()
            2. Instatiates a Token agent for each whole token it controls
        '''
        if self.tokens >= 1:
            self.belief = self.get_belief()
            for i in range(0,int(self.tokens)):
                token = Token(self.model.next_id(), self.model, self)
                self.model.schedule.add(token)
