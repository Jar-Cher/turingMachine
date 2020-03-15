# Copyright (C) 2020 luna_koly
#
# A simple example of a machine that
# always goes right and prints either 'X'
# or 'Y' depending on which one of these
# it saw the last time.


from turing import TuringMachine
from lnr import LNRState


ANY = None
KEEP = None

L = 'l'
R = 'r'
N = 'n'

B = '.'
X = 'X'
Y = 'Y'
E = 'E'


FLIPPER_ALPHABET = [
    B, X, Y, E
]


class FlipperState(LNRState):
    '''
    A state of a machine that
    always goes right and prints either 'X'
    or 'Y' depending on which one of these
    it saw the last time.
    '''
    def start_flips(self):
        PRINT_X = self
        PRINT_Y = self.state()
        END = self.state()

        PRINT_X.on(ANY).cycle(R, X)
        PRINT_X.on(Y).go(R, PRINT_Y)
        PRINT_X.on(E).go(R, END)

        PRINT_Y.on(ANY).cycle(R, Y)
        PRINT_Y.on(X).go(R, PRINT_X)
        PRINT_Y.on(E).go(R, END)

        return END


class FlipperMachine(TuringMachine):
    '''
    A machine that
    always goes right and prints either 'X'
    or 'Y' depending on which one of these
    it saw the last time.
    '''
    def __init__(self):
        super().__init__(FLIPPER_ALPHABET, FlipperState)
        self.BEGIN.start_flips().end()
