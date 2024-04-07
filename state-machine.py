from transitions import Machine, core
import fileinput


# Using dummy name for class with properties and methods that the
# framework binds and we expect to access. We do this so pyright
# type inference doesn't generate errors.
class Matter(object):
    rdata = 0
    sdata = 0

    # Native package events are different from ours
    # Incrementing should be done elsewhere
    def log(self, event):
        name = event.event.name
        if name == "RDATA":
            self.rdata += 1
            print(f"DATA received {self.rdata}")
        elif name == "SDATA":
            self.sdata += 1
            print(f"DATA sent {self.sdata}")
        else:
            print(f"Event {name} received, current State is {lump.state}")


lump = Matter()

states = [
    "CLOSED",
    "LISTEN",
    "SYN_SENT",
    "SYN_RCVD",
    "ESTABLISHED",
    "FIN_WAIT_1",
    "FIN_WAIT_2",
    "CLOSING",
    "TIME_WAIT",
    "CLOSE_WAIT",
    "LAST_ACK",
]

transitions = [
    # Don't implement LISTEN to SYN_SENT transition
    {"trigger": "PASSIVE", "source": "CLOSED", "dest": "LISTEN"},
    {"trigger": "CLOSE", "source": "LISTEN", "dest": "CLOSED"},
    {"trigger": "ACTIVE", "source": "CLOSED", "dest": "SYN_SENT"},
    {"trigger": "CLOSE", "source": "SYN_SENT", "dest": "CLOSED"},
    {"trigger": "SYN", "source": "LISTEN", "dest": "SYN_RCVD"},
    {"trigger": "SYN", "source": "SYN_SENT", "dest": "SYN_RCVD"},
    {"trigger": "ACK", "source": "SYN_RCVD", "dest": "ESTABLISHED"},
    {"trigger": "SYNACK", "source": "SYN_SENT", "dest": "ESTABLISHED"},
    {"trigger": "CLOSE", "source": "SYN_RCVD", "dest": "FIN_WAIT_1"},
    {"trigger": "CLOSE", "source": "ESTABLISHED", "dest": "FIN_WAIT_1"},
    {"trigger": "FIN", "source": "ESTABLISHED", "dest": "CLOSE_WAIT"},
    # These are supported as reflexive transitions
    {"trigger": "RDATA", "source": "ESTABLISHED", "dest": "="},
    {"trigger": "SDATA", "source": "ESTABLISHED", "dest": "="},
    {"trigger": "ACK", "source": "FIN_WAIT_1", "dest": "FIN_WAIT_2"},
    {"trigger": "FIN", "source": "FIN_WAIT_1", "dest": "CLOSING"},
    {"trigger": "CLOSE", "source": "CLOSE_WAIT", "dest": "LAST_ACK"},
    {"trigger": "FIN", "source": "FIN_WAIT_2", "dest": "TIME_WAIT"},
    {"trigger": "ACK", "source": "CLOSING", "dest": "TIME_WAIT"},
    # Diagram should map back to original CLOSED box
    {"trigger": "ACK", "source": "LAST_ACK", "dest": "CLOSED"},
    {"trigger": "TIMEOUT", "source": "TIME_WAIT", "dest": "CLOSED"},
]

machine = Machine(
    lump,
    states=states,
    transitions=transitions,
    initial="CLOSED",
    # Required for reading events
    send_event=True,
    after_state_change="log",
)

valid_events = [
    "PASSIVE",
    "CLOSE",
    "ACTIVE",
    "SYN",
    "ACK",
    "SYNACK",
    "FIN",
    "RDATA",
    "SDATA",
    "TIMEOUT",
]


# Read events from standard input
# We should exit when reaching end of input stream
# Using a separate function for scoping
def read():
    for line in fileinput.input():
        events = line.split()
        for event in events:
            if event not in valid_events:
                print(f"Error: unexpected Event: {event}")
                continue
            # Events that are valid but not allowed for a specific state
            # trigger exceptions we need to catch to ensure recovery
            try:
                # lump.trigger("PASSIVE")
                lump.trigger(event)
            except core.MachineError as e:
                print(e)
                continue


read()
