from turing import TuringMachine
from lnr import LNRState

ANY = None
KEEP = None

L = 'l'
R = 'r'
N = 'n'

B = '.'
l = '1'
lx = '1x'
T = 'T'     # метка второго слагаемого
t = 't'     # метка первого слагаемого
S = 'S'     # метка конструируемой суммы
E = 'E'     # метка конца последовательности
N = 'N'     # метка текущего рассматриваемого числа

GOLD_ALPHABET = [
    B, lx, l, t, T, S, E, N
]


class GoldState(LNRState):


    def incrementNum(self):
        INCREMENT = self
        ENLARGE = self.state()
        STOP = self.state()

        (INCREMENT.move_right_until(E, overstep=L).step_right()
            .drop(l, R).drop(l, R).drop(l, R).drop(E, L).on(ANY).go(L, ENLARGE))

        (ENLARGE.move_left_until(N, overstep=L).step_right().drop(B, R).drop(B, R).drop(N, R).on(ANY).go(L, STOP))

        return STOP

    def copyNum(self):
        INIT = self
        STOP = self.state()
        UNMARK = self.state()
        FINISH = self.state()

        SEARCH = INIT.move_right_until(E, overstep=L).move_left_while(lx, overstep=R).step_left()
        SEARCH.on(N).go(R, UNMARK)
        (SEARCH.on(l).new(R).step_left()
            .drop(lx, L).move_left_until(E, overstep=L)
            .move_left_until(B, overstep=R).step_left().drop(l, R)
            .move_right_until(N, overstep=L).on(ANY).go(R, INIT))

        UNMARK.on(ANY).go(L, FINISH)
        UNMARK.on(lx).cycle(R, l)

        (FINISH.move_left_until(E, overstep=L).step_left().move_left_while(l, overstep=L)
            .step_right().drop(N, R).on(ANY).go(R, STOP))

        return STOP

    def main(self):
        COUNTER = self
        END = self.state()

        COUNTER.copyNum().on(ANY).go(L, END)

        return END


class GoldMachine(TuringMachine):
    '''

    '''

    def __init__(self):
        super().__init__(GOLD_ALPHABET, GoldState)
        self.BEGIN.main().end()
