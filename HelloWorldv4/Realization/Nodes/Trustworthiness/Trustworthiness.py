# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.clientLibraries.rpclpy.node import Node
import time

try:
    from .messages import *
except (ValueError, ImportError):
    from messages import *

#<!-- cc_include START--!>
# user includes here
#<!-- cc_include END--!>

#<!-- cc_code START--!>
# user code here
#<!-- cc_code END--!>

class Trustworthiness(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "Trustworthiness"
        self.logger.info("Trustworthiness instantiated")

        #<!-- cc_init START--!>
        # user includes here
        #<!-- cc_init END--!>

    # -----------------------------AUTO-GEN SKELETON FOR t_a-----------------------------
    def t_a(self,msg):
        _Direction = Direction()

        #<!-- cc_code_t_a START--!>

        # user code here for t_a

        _Direction._omega= "SET VALUE"    # datatype: Float_64
        _Direction._duration= "SET VALUE"    # datatype: Float_64

        #<!-- cc_code_t_a END--!>

        # TODO: Put desired publish event inside user code and uncomment!!
        #self.publish_event(event_key='stage',message=_Direction)    # LINK <outport> stage
    # -----------------------------AUTO-GEN SKELETON FOR t_p-----------------------------
    def t_p(self,msg):
        _Direction = Direction()

        #<!-- cc_code_t_p START--!>

        # user code here for t_p

        _Direction._omega= "SET VALUE"    # datatype: Float_64
        _Direction._duration= "SET VALUE"    # datatype: Float_64

        #<!-- cc_code_t_p END--!>

        # TODO: Put desired publish event inside user code and uncomment!!
        #self.publish_event(event_key='stage',message=_Direction)    # LINK <outport> stage
    # -----------------------------AUTO-GEN SKELETON FOR t_l-----------------------------
    def t_l(self,msg):
        _Direction = Direction()

        #<!-- cc_code_t_l START--!>

        # user code here for t_l

        _Direction._omega= "SET VALUE"    # datatype: Float_64
        _Direction._duration= "SET VALUE"    # datatype: Float_64

        #<!-- cc_code_t_l END--!>

        # TODO: Put desired publish event inside user code and uncomment!!
        #self.publish_event(event_key='stage',message=_Direction)    # LINK <outport> stage
    # -----------------------------AUTO-GEN SKELETON FOR t_e-----------------------------
    def t_e(self,msg):
        spin_config = self.knowledge.read("spin_config",queueSize=1)
        _Direction = Direction()

        #<!-- cc_code_t_e START--!>

        # user code here for t_e

        _Direction._omega= "SET VALUE"    # datatype: Float_64
        _Direction._duration= "SET VALUE"    # datatype: Float_64

        #<!-- cc_code_t_e END--!>

        # TODO: Put desired publish event inside user code and uncomment!!
        #self.publish_event(event_key='stage',message=_Direction)    # LINK <outport> stage
    # -----------------------------AUTO-GEN SKELETON FOR trust_check-----------------------------
    def trust_check(self,msg):

        #<!-- cc_code_trust_check START--!>

        # user code here for trust_check
        self.logger.info("Trustworthiness check initiated")
        

        #<!-- cc_code_trust_check END--!>

        # TODO: Put desired publish event inside user code and uncomment!!

    def register_callbacks(self):
        self.register_event_callback(event_key='anomaly', callback=self.t_a)     # LINK <eventTrigger> anomaly
        self.register_event_callback(event_key='anomaly', callback=self.t_a)        # LINK <inport> anomaly
        self.register_event_callback(event_key='new_plan', callback=self.t_p)     # LINK <eventTrigger> new_plan
        self.register_event_callback(event_key='new_plan', callback=self.t_p)        # LINK <inport> new_plan
        self.register_event_callback(event_key='isLegit', callback=self.t_l)     # LINK <eventTrigger> isLegit
        self.register_event_callback(event_key='isLegit', callback=self.t_l)        # LINK <inport> isLegit
        self.register_event_callback(event_key='spin_config', callback=self.t_e)     # LINK <eventTrigger> spin_config
        self.register_event_callback(event_key='spin_config', callback=self.t_e)        # LINK <inport> spin_config
        self.register_event_callback(event_key='maple', callback=self.trust_check)     # LINK <eventTrigger> maple
        self.register_event_callback(event_key='maple', callback=self.trust_check)        # LINK <inport> maple

def main(args=None):

    node = Trustworthiness(config='config.yaml')
    node.register_callbacks()
    node.start()

if __name__ == '__main__':
    main()
    try:
       while True:
           time.sleep(1)
    except:
       exit()