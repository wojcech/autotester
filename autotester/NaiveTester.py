from datetime import datetime
from .abstractions import *
from .helpers import mytimestamp


class NaiveTester(object):

    def __init__(self, state_estimator, planner, executor,notificator,memory):
        self.next_id =1
        self.test_log =[]

        self.memory =memory
        self.estimator=state_estimator
        self.planner = planner
        self.executor = executor
        self.notificator = notificator



    def run(self,CURRENT_SAMPLE, max_steps=100,startState=None):
        self.memory.CURRENT_SAMPLE=CURRENT_SAMPLE
        self.executor.CURRENT_SAMPLE=CURRENT_SAMPLE



        curstate=self.estimator.estimate_state(None,startState)
        print("StartState",curstate)
        adaptation = Adaptations.NOCHANGE
        next_action= self.planner.get_action(curstate)
        print("Action",next_action)
        step=0
        while next_action is not None and step < max_steps:
            new_datum = self.executor.execute(adaptation,next_action)
            print("Datum",new_datum)
            new_state = self.estimator.estimate_state(new_datum,curstate)
            self.memory.log(adaptation,next_action,self.curstate,new_state,self.executor.pulseControl,self.executor.sweepControl)  # NOTE XXX bit of an ugliness to reach into executor, might be worth to refactor
            self.curstate=new_state
            print("NewState",self.curstate)
            adaptation = self.planner.get_adaptation(next_action,self.curstate)
            next_action= self.planner.get_action(self.curstate)
            print("Adaptation",adaptation)
            print("Action",next_action)
            step+=1
        self.memory.save_log()
        self.notificator.done()
