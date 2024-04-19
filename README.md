# tcp-fsm

Finite State Machine for the TCP Connection Protocol

## Description

This package implements a Finite State Machine for the TCP Connection Protocol.
This state machine is built using Python with the help of the
[`transitions`](https://github.com/pytransitions/transitions) package. For
supported states and events see the lists below.

### Supported states

- CLOSED
- LISTEN
- SYN_SENT
- SYN_RCVD
- ESTABLISHED
- FIN_WAIT_1
- FIN_WAIT_2
- CLOSING
- TIME_WAIT
- CLOSE_WAIT
- LAST_ACK

### Supported events

- PASSIVE
- CLOSE
- ACTIVE
- SYN
- ACK
- SYNACK
- FIN
- RDATA
- SDATA
- TIMEOUT

## Requirements

Python 3.11.3 or later

## Setup

``` sh
pip install -r requirements.txt
```

## Running

``` sh
python state-machine.py
```

The following format also works:

``` sh
echo "PASSIVE\nCLOSE" | python state-machine.py
echo "PASSIVE CLOSE" | python state-machine.py
cat test.txt | python state-machine.py
```

## Using

After running the above program, it will start waiting to accept input from
`stdin` . You can enter any of the supported events that apply to a given
state to transition the state machine from one state to another.

- Events must be UPPERCASE like those shown above
- Events must be separated by whitespace (eg. space, newline)

After an event is entered and whitespace or a newline character is processed,
the state machine will execute for that event. If the event is supported and
applies to the current state, the state machine will transition to the new
state and print the change to the console.

- Successful transition: Event {name} received, current State is {state}
- Received RDATA: DATA received {rdata}
- Sent SDATA: DATA sent {sdata}

If any event is not supported or the event is supported but doesn't apply to
the current state, the program will print an error message with an explanation
and continue to allow further input.

- Unsupported event: Error: unexpected Event: {event}
- Caught exception: "Can't trigger event {event} from state {state}!"

## Design

This state machine is implemented using the `transitions` package and therefore
might differ in the names for some concepts used in other state machines.

- States: Represent the allowed configurations of the machine
- Events: Represent the allowed inputs that the machine will recognize
- Transitions: Represent the allowed changes from one state to another. These
  are defined by specifying an event, source, and destination.
- Callbacks: Represent "Actions" that are executed for a transition
- `MachineError`: Errors raised in the machine analogous to `FsmException`
