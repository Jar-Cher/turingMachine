from turing import TuringMachine
from lnr import LNRState

ANY = None
KEEP = None

L = 'l'
R = 'r'
N = 'n'

B = '.'
N1 = '1'
N2 = '2'
N3 = '3'
N4 = '4'
N5 = '5'
N6 = '6'
N7 = '7'
N8 = '8'
N9 = '9'
N0 = '0'
S = 'S'

GOLD_ALPHABET = [
    B, N0, N1, N2, N3, N4, N5, N6, N7, N8, N9, S
]


class GoldState(LNRState):
    '''
    Функция инкрементирует число формата S [1-9]+ B* S
    При этом начальное и конечное положение головки при выполнении функции указывает на младший разряд
    '''

    def copyRight(self):
        SITUATION = self
        STOP = self.state()

        SITUATION.on(B)
    def increment(self):
        NEWNUM = self
        STOP = self.state()

        # Просто инкрементация младшего разряда != 9
        NEWNUM.on(N0).new(R, symbol=N1).on(ANY).go(L, STOP)
        NEWNUM.on(N1).new(R, symbol=N2).on(ANY).go(L, STOP)
        NEWNUM.on(N2).new(R, symbol=N3).on(ANY).go(L, STOP)
        NEWNUM.on(N3).new(R, symbol=N4).on(ANY).go(L, STOP)
        NEWNUM.on(N4).new(R, symbol=N5).on(ANY).go(L, STOP)
        NEWNUM.on(N5).new(R, symbol=N6).on(ANY).go(L, STOP)
        NEWNUM.on(N6).new(R, symbol=N7).on(ANY).go(L, STOP)
        NEWNUM.on(N7).new(R, symbol=N8).on(ANY).go(L, STOP)
        NEWNUM.on(N8).new(R, symbol=N9).on(ANY).go(L, STOP)

        # Но если в младшем разряде 9, идём смотреть символ после самой старшей девятки
        NEXTDIGITTOINCREMENT = (NEWNUM.on(N9).new(R, symbol=N9).step_left()
                                .move_left_while(N9, overstep=R).step_left()
        )

        # Увеличиваем самый старший ненулевой символ-число и идём к самому младшему, заменяя девятки на нули
        NEXTDIGITTOINCREMENT.on(N0).new(R, symbol=N1).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N1).new(R, symbol=N2).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N2).new(R, symbol=N3).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N3).new(R, symbol=N4).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N4).new(R, symbol=N5).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N5).new(R, symbol=N6).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N6).new(R, symbol=N7).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N7).new(R, symbol=N8).on(N9).cycle(R, N0).on(ANY).go(L, STOP)
        NEXTDIGITTOINCREMENT.on(N8).new(R, symbol=N9).on(N9).cycle(R, N0).on(ANY).go(L, STOP)

        # Увеличиваем разрядность
        (NEXTDIGITTOINCREMENT.on(S).new(R, symbol=S).drop(N1, R).on(N9).cycle(R, N0)
         .drop(N0, R).drop(S, R).step_left().on(ANY).go(L, STOP))
        '''
        INCREMENTINGDIGIT = (NEXTDIGITTOINCREMENT.on(ANY).new(R)
                .move_right_until(S, overstep=R).step_left().step_left()
                .move_left_while(B, overstep=R).step_left()
                .move_left_while(N9, overstep=R).step_left()
        )

        INCREMENTINGDIGIT.on(N0).new(R, symbol=N1).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N1).new(R, symbol=N2).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N2).new(R, symbol=N3).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N3).new(R, symbol=N4).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N4).new(R, symbol=N5).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N5).new(R, symbol=N6).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N6).new(R, symbol=N7).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N7).new(R, symbol=N8).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)
        INCREMENTINGDIGIT.on(N8).new(R, symbol=N9).on(N9).cycle(R, N0).step_left().on(ANY).go(R, STOP)

        LOCALEXPANSION = NEXTDIGITTOINCREMENT.on(N9).new(R, symbol=N1)

        LOCALEXPANSION.on(N9).cycle(R, N0)
        LOCALEXPANSION.on(B).new(R, symbol=N0).on(ANY).go(L, STOP)  # TO FIX
        LOCALEXPANSION.on(S).new(R, symbol=N0).on(ANY).new(R,symbol=S).step_left().on(ANY).go(L, STOP)
        '''
        return STOP

    def main(self):
        COUNTER = self
        END = self.state()

        COUNTER.increment().increment().on(ANY).go(L, END)

        return END


class GoldMachine(TuringMachine):
    '''

    '''

    def __init__(self):
        super().__init__(GOLD_ALPHABET, GoldState)
        self.BEGIN.main().end()
