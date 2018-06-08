# coding=utf-8

"""Main Process Handler managing communication from GUI to all child processes"""

import time
import multiprocessing as mp
from Misc.GlobalVars import *
from Misc.CustomClasses import *
import queue as Queue


class ProcessHandler(StoppableProcess):
    """Main handler class with communication protocols to child processes"""
    def __init__(self, cmr_msgs, cmr_vidrec_msgs, *msg_rcvd_pipes):
        super(ProcessHandler, self).__init__()
        self.input_msgs = PROC_HANDLER_QUEUE
        self.exp_start_event = EXP_START_EVENT
        self.msg_rcvd_pipes = msg_rcvd_pipes
        self.vidrec_saving_list = []
        self.vidrec_finished_list = []
        self.queue_selector = {
            PROC_CMR: cmr_msgs,
            PROC_CMR_VIDREC: cmr_vidrec_msgs,
            PROC_GUI: MASTER_DUMP_QUEUE
        }

    def setup_msg_parser(self):
        """Dictionary of {Msg:Actions}"""
        self.msg_parser = {
            # Messages with general destinations
            CMD_START: lambda d, params: self.run_experiment(run=True, trial_params=params),
            CMD_STOP: lambda d, v: self.run_experiment(run=False),
            CMD_EXIT: lambda d, v: self.close_children(),
            # Messages bound for GUI
            MSG_VIDREC_SAVING: lambda proc_origin, v: self.vidrec_saving(saving=True, proc_origin=proc_origin),
            MSG_VIDREC_FINISHED: lambda proc_origin, v: self.vidrec_saving(saving=False, proc_origin=proc_origin),
        }

    def process_message(self, msg):
        """Follows instructions in queue message"""
        self.msg_parser[msg.command](msg.device, msg.value)

    def send_message(self, targets, cmd=None, val=None):
        """Sends a message to children"""
        msg = NewMessage(cmd=cmd, val=val)
        for target in targets:
            self.queue_selector[target].put_nowait(msg)

    def run(self):
        """Called by start(), spawns new process"""
        self.setup_msg_parser()
        while not self.stopped():
            try:
                msg = self.input_msgs.get(timeout=0.5)
            except Queue.Empty:
                time.sleep(1.0 / 1000.0)
            else:
                msg = ReadMessage(msg)
                self.process_message(msg)
        print('Exiting Process Handler...')

    def close_children(self):
        """Close all child processes before exiting"""
        self.send_message(targets=(PROC_CMR, PROC_CMR_VIDREC), cmd=CMD_EXIT)
        self.stop()

    # Experiment running functions
    def run_experiment(self, run, trial_params=None):
        """Tells child widgets to start/stop experiment"""
        # Start
        if run:
            self.exp_start_event.clear()
            self.send_message(targets=(PROC_CMR_VIDREC,),
                              cmd=CMD_START,
                              val=trial_params)
            for pipe in self.msg_rcvd_pipes:
                pipe.recv()
            # don't allow any process to proceed unless all processes have confirmed receipt of message
            self.exp_start_event.set()
            # Once exp_start_event is set, we can let master gui know that we've begun recording/etc.
            self.send_message(targets=(PROC_GUI,), cmd=MSG_STARTED)
        # Forced stop
        elif not run:
            self.exp_start_event.clear()
            self.send_message(targets=(PROC_CMR_VIDREC,),
                              cmd=CMD_STOP)

    def vidrec_saving(self, saving, proc_origin):
        """collects all CMD_VIDREC_SAVING and CMD_VIDREC_SAVED signals, then sends a single signal
        to GUI when all signals are collected"""
        if saving:
            self.vidrec_saving_list.append(proc_origin)
            if PROC_CV2_VIDREC in self.vidrec_saving_list\
                    and PROC_CMR_VIDREC in self.vidrec_saving_list\
                    and PROC_COORDS in self.vidrec_saving_list:
                self.vidrec_saving_list = []
                self.send_message(targets=(PROC_GUI,), cmd=MSG_VIDREC_SAVING)
        elif not saving:
            self.vidrec_finished_list.append(proc_origin)
            if PROC_CV2_VIDREC in self.vidrec_finished_list\
                    and PROC_CMR_VIDREC in self.vidrec_finished_list\
                    and PROC_COORDS in self.vidrec_finished_list:
                self.vidrec_finished_list = []
                self.send_message(targets=(PROC_GUI,), cmd=MSG_VIDREC_FINISHED)
