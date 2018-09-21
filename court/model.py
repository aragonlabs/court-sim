import random
import math
import mesa

from mesa import Model
from mesa.datacollection import DataCollector

from court.agents import Juror, Token
from court.scheduler import CourtScheduler

#Global variables
base_dispute_size = 5

def compute_gini(model):
    juror_tokens = [juror.tokens for juror in model.schedule.jurors.values()]
    x = sorted(juror_tokens)
    print(x)
    N = model.juror_count
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    print(B)
    return (1 + (1 / N) - 2 * B)

class CourtModel(Model):
    """A model of a decentralized oracle for subjective disputes."""
    def __init__(self, juror_count=20, token_count=40, belief_deviation=0.3, penalty_pct=0.5, threshold=0.5, base_dispute_size=5):
        super().__init__()
        self.schedule = CourtScheduler(self, base_dispute_size )
        self.current_id = 0

        self.penalty_pct = penalty_pct
        self.threshold = 0.2
        self.belief_deviation = belief_deviation
        self.juror_count = juror_count
        self.token_count = token_count

        self.dispute_level = 1
        self.true_votes = 0
        self.false_votes = 0

        self.disputes = 0
        self.successful = 0
        self.failed = 0

        #self.datacollector = DataCollector({"Gini": compute_gini} )

        for j in range(0,juror_count):
            juror = Juror(self.next_id(), self, self.belief_deviation)
            self.schedule.add(juror)

        self.running = True

        self.datacollector = DataCollector({"Gini": compute_gini ,"total":"disputes", "successful":"successful", "failed":"failed"})

    def next_id(self):
        """ Return the next unique ID for agents, increment current_id"""
        self.current_id += 1
        return self.current_id

    def new_dispute(self):
        self.true_value = random.randint(0,1)
        self.true_votes = 0
        self.false_votes = 0
        self.dispute_level = 1
        self.disputes += 1
        self.schedule.step()

    def appeal(self):
        self.dispute_level += 1
        self.schedule.step()

    def vote(self, value):
        """
        Called by activated agents to register their vote with model
        """
        if value:
            self.true_votes += 1
        else:
            self.false_votes += 1

    def result(self):
        """ Returns true if true vote wins, false if false vote won """
        return self.true_votes > self.false_votes

    def step(self):
        '''
        Run one step of the model.
        '''
        print("Gini: " + str(compute_gini(self)))
        print("Dispute: " + str(self.disputes))
        print("Dispute Level: " + str(self.dispute_level))
        print("Successful Verdict: " + str(self.result()) + " Votes: " + str(self.true_votes) + str(self.false_votes))

        if self.disputes == 0:
            self.new_dispute()
        elif self.result() == True or self.false_votes + self.true_votes >= self.schedule.get_type_count('Token'):
            if self.result():
                self.successful+=1
            else:
                self.failed +=1
            self.schedule.reward()
            self.new_dispute()
        else:
            self.appeal()

        self.datacollector.collect(self)
