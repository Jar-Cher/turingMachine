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
C = 'C'
c = 'c'
T = 'T'     # метка второго слагаемого
t = 't'     # метка первого слагаемого
S = 'S'     # метка конструируемой суммы
E = 'E'     # метка конца последовательности
N = 'N'     # метка текущего рассматриваемого числа

GOLD_ALPHABET = [
    B, lx, l, t, T, S, E, N, c, C
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


    def decrementTerm(self):
        INIT = self
        STOP = self.state()

        INIT.move_left_until(N, overstep=R).step_left().step_right().drop(N, L).drop(B, R).on(ANY).go(R, STOP)

        return STOP


    def prepareIteration(self):
        INIT = self
        STOP = self.state()

        INIT.move_right_until(S, overstep=L).drop(c, L).drop(C, R).on(ANY).go(L, STOP)

        return STOP


    def copyFactor(self):
        INIT = self
        STOP = self.state()
        UNMARK = self.state()
        FINISH = self.state()

        SEARCH = INIT.move_right_until(C, overstep=L).move_left_while(lx, overstep=R).step_left()
        SEARCH.on(E).go(R, UNMARK)
        SEARCH.on(t).go(R, UNMARK)
        (SEARCH.on(l).new(R).step_left()
         .drop(lx, L).move_left_until(N, overstep=L)
         .move_left_until(B, overstep=R).step_left().drop(l, R)
         .move_right_until(C, overstep=L).on(ANY).go(R, INIT))

        UNMARK.on(ANY).go(L, FINISH)
        UNMARK.on(lx).cycle(R, l)

        FINISH.move_left_until(B, overstep=L).step_right().on(ANY).go(R, STOP)

        return STOP


    def checkDivider(self):
        INIT = self
        STARTDIV = self.state()
        CHECK = self.state()
        DECREASE = self.state()
        STOP = self.state()

        STARTDIV = INIT.move_right_while(lx, overstep=R).step_left()

        DECREASE = (STARTDIV.on(l).new(R).step_left()
         .drop(lx, L).move_right_until(E, overstep=L)
         .move_left_while(lx, overstep=R).step_left())

        CHECK = DECREASE.on(l).new(R).step_left().drop(lx, L)

        CHECK.on(l).new(L).move_left_until(B, overstep=R).on(ANY).go(R, INIT)
        CHECK.on(N).go(L, STOP)

        STARTDIV.on(N).new(R).step_left().step_left().on(lx).cycle(L, l).on(ANY).go(R, INIT)

        return STOP


    def clearFactor(self):
        INIT = self
        STOP = self.state()

        (INIT.move_left_until(B, overstep=R).on(lx).cycle(R, B).on(l).cycle(R, B)
         .step_right().on(lx).cycle(R, l).on(ANY).go(L, STOP))

        return STOP


    def checkNextFactor(self):
        INIT = self
        STOP = self.state()

        INIT.move_right_until(C, overstep=L).move_left_while(l, overstep=L).on(ANY).go(R, STOP)

        return STOP


    def iterateFactor(self):
        INIT = self
        STOP = self.state()

        (INIT.move_right_until(c, overstep=R).step_left().drop(t, L).drop(T, L)
         .move_left_until(t, overstep=R).step_left().drop(c, L).drop(C, L).on(ANY).go(R, STOP))

        return STOP


    def savePrime(self):
        INIT = self
        STOP = self.state()

        (INIT.step_right().drop(t, L).drop(T, L)
         .move_left_until(N, overstep=L).drop(E, R).drop(E, R)
         .move_right_until(C, R).drop(t, L).drop(T, R).on(ANY).go(L, STOP))

        return STOP


    def deleteNonPrime(self):
        INIT = self
        STOP = self.state()

        (INIT.move_right_until(E, overstep=L).on(l).cycle(L, B).drop(B, R)
         .move_right_until(C, overstep=R).drop(t, L).drop(T, R).on(ANY).go(L, STOP))

        return STOP

    def copyc(self):
        INIT = self
        STOP = self.state()
        UNMARK = self.state()

        SEARCH = INIT.move_left_until(c, overstep=L).step_left().move_left_while(lx, overstep=R).step_left()
        SEARCH.on(E).go(R, UNMARK)
        SEARCH.on(t).go(R, UNMARK)
        (SEARCH.on(l).new(R).step_left()
         .drop(lx, L).move_right_until(S, overstep=R)
         .move_right_while(l, overstep=R).step_left().drop(l, R)
         .on(ANY).go(R, INIT))

        UNMARK.on(ANY).go(L, STOP)
        UNMARK.on(lx).cycle(R, l)

        return STOP


    def copyC(self):
        INIT = self
        STOP = self.state()
        UNMARK = self.state()

        SEARCH = INIT.move_left_until(C, overstep=L).move_left_while(lx, overstep=R).step_left()
        SEARCH.on(E).go(R, UNMARK)
        SEARCH.on(t).go(R, UNMARK)
        SEARCH.on(c).go(R, UNMARK)
        (SEARCH.on(l).new(R).step_left()
         .drop(lx, L).move_right_until(S, overstep=R)
         .move_right_while(l, overstep=R).step_left().drop(l, R)
         .on(ANY).go(R, INIT))

        UNMARK.on(ANY).go(L, STOP)
        UNMARK.on(lx).cycle(R, l)

        return STOP


    def compare(self):
        INIT = self
        STOP = self.state()
        #CHECK = self.state()
        AFTERCHECK = self.state()
        NEXTSYMBOL = self.state()

        SEARCH = INIT.move_right_while(lx, overstep=R).step_left()
        SEARCH.on(B).go(L, AFTERCHECK)
        (SEARCH.on(l).new(R).step_left()
         .drop(lx, L).move_right_until(N, overstep=R)
         .move_right_while(lx, overstep=R).on(ANY).go(L, NEXTSYMBOL))

        NEXTSYMBOL.on(l).new(R).step_left().drop(lx, R).move_left_until(S, overstep=R).step_left().on(ANY).go(R, INIT)
        NEXTSYMBOL.on(E).new(L).drop(l, R).on(ANY).go(L, STOP)

        #CHECK.on(l).new(R).move_left_until(S, overstep=R).step_left().on(ANY).go(R, INIT)
        #CHECK.on(E).go(L, AFTERCHECK)

        AFTERCHECK.move_right_until(E, overstep=R).step_left().on(ANY).go(L, STOP)

        return STOP


    def clearSum(self):
        INIT = self
        CLEARNUM = self.state()
        CLEARSUM = self.state()
        STOP = self.state()

        INIT.move_right_until(E, overstep=L).step_right().on(ANY).go(L, CLEARNUM)

        CLEARNUM.on(l).cycle(L, l)
        CLEARNUM.on(lx).cycle(L, l)
        CLEARNUM.on(N).go(L, CLEARSUM)

        CLEARSUM.on(B).cycle(L, B)
        CLEARSUM.on(l).cycle(L, B)
        CLEARSUM.on(lx).cycle(L, B)
        CLEARSUM.on(S).go(L, STOP)

        return STOP


    def finishIteration(self):
        INIT = self
        CLEARNUM = self.state()
        CLEARSUM = self.state()
        STOP = self.state()

        (INIT.move_right_until(S, overstep=R).move_left_until(c, overstep=R).step_left()
         .drop(t, L).move_right_until(S, overstep=R).move_left_until(C, overstep=R).step_left()
         .drop(T, L).on(ANY).go(R, STOP))

        return STOP

    def checkNextc(self):
        INIT = self
        STOP = self.state()

        INIT.move_left_until(c, overstep=L).step_left().move_left_while(l, overstep=L).on(ANY).go(R, STOP)

        return STOP


    def checkNextC(self):
        INIT = self
        STOP = self.state()

        INIT.move_left_until(C, overstep=L).move_left_while(l, overstep=L).step_left().on(ANY).go(R, STOP)

        return STOP

    def resetc(self):
        INIT = self
        STOP = self.state()

        (INIT.move_right_until(c, overstep=R).step_left().drop(t, L)
         .move_right_until(S, overstep=L).drop(c, L).on(ANY).go(R, STOP))

        return STOP

    def iteratec(self):
        INIT = self
        STOP = self.state()

        (INIT.move_right_until(c, overstep=R).step_left().drop(t, L)
         .move_left_until(t, overstep=R).step_left().drop(c, L).on(ANY).go(R, STOP))

        return STOP


    def iterateC(self):
        INIT = self
        STOP = self.state()

        (INIT.move_right_until(C, overstep=R).step_left().drop(T, L)
         .move_left_until(T, overstep=R).step_left().drop(C, L).on(ANY).go(R, STOP))

        return STOP


    def main(self):
        INIT = self
        PREPARATION1 = self.state()
        PREPARATION2 = self.state()
        FIRSTNUMBERCHECK1 = self.state()
        FIRSTNUMBERCHECK2 = self.state()
        CHECKDIVIDER1 = self.state()
        CHECKDIVIDER2 = self.state()
        CHECKINGDIVIDER1 = self.state()
        CHECKINGDIVIDER2 = self.state()
        CHECKNEXTFACTOR1 = self.state()
        CHECKNEXTFACTOR2 = self.state()
        ITERATE1 = self.state()
        ITERATE2 = self.state()
        DELETE1 = self.state()
        DELETE2 = self.state()
        SAVE1 = self.state()
        SAVE2 = self.state()
        PREPARESUM = self.state()
        SUMCYCLE = self.state()
        COMPARED = self.state()
        CHECKINGC = self.state()
        FINISH = self.state()
        END = self.state()

        INIT.incrementNum().incrementNum().copyNum().decrementTerm().prepareIteration().on(ANY).go(L, CHECKINGDIVIDER1)

        CHECKINGDIVIDER1.copyFactor().checkDivider().step_right().on(ANY).go(L, CHECKDIVIDER1)

        CHECKDIVIDER1.on(l).new(R).clearFactor().checkNextFactor().step_right().on(ANY).go(L, CHECKNEXTFACTOR1)
        CHECKDIVIDER1.on(lx).new(R).clearFactor().on(ANY).go(L, DELETE1)               # not prime

        CHECKNEXTFACTOR1.on(E).go(L, SAVE1)                                            # prime
        CHECKNEXTFACTOR1.on(t).go(L, ITERATE1)                                         # inconclusive so far

        ITERATE1.iterateFactor().on(ANY).go(L, CHECKINGDIVIDER1)

        DELETE1.deleteNonPrime().on(ANY).go(L, PREPARATION2)
        SAVE1.savePrime().on(ANY).go(L, PREPARATION2)

        PREPARATION2.copyNum().prepareIteration().on(ANY).go(L, CHECKINGDIVIDER2)

        CHECKINGDIVIDER2.copyFactor().checkDivider().step_right().on(ANY).go(L, CHECKDIVIDER2)

        CHECKDIVIDER2.on(l).new(R).clearFactor().checkNextFactor().step_right().on(ANY).go(L, CHECKNEXTFACTOR2)
        CHECKDIVIDER2.on(lx).new(R).clearFactor().on(ANY).go(L, DELETE2)               # not prime

        CHECKNEXTFACTOR2.on(E).go(L, SAVE2)                                            # prime
        CHECKNEXTFACTOR2.on(t).go(L, ITERATE2)                                         # inconclusive so far

        ITERATE2.iterateFactor().on(ANY).go(L, PREPARATION2)

        DELETE2.deleteNonPrime().on(ANY).go(L, PREPARESUM)
        SAVE2.savePrime().on(ANY).go(L, PREPARESUM)

        PREPARESUM.prepareIteration().on(ANY).go(L, SUMCYCLE)

        (SUMCYCLE.move_right_until(S, overstep=R).copyc()
         .move_right_until(S, overstep=R).copyC()
         .move_right_until(S, overstep=R).compare().step_right().on(ANY).go(L, COMPARED))

        COMPARED.on(lx).go(L, FINISH)

        CHECKINGc = COMPARED.on(l).new(L).clearSum().checkNextc()

        CHECKINGc.on(t).new(L).iteratec().on(ANY).go(L, SUMCYCLE)
        (CHECKINGc.on(E).new(L).resetc()
         .move_right_until(S, overstep=R).checkNextC().step_right().on(ANY).go(L, CHECKINGC))

        CHECKINGC.on(E).go(L, END)                       # В исторические времена мы сюда не доберемся
        CHECKINGC.on(T).new(L).iterateC().on(ANY).go(L, SUMCYCLE)

        FINISH.clearSum().finishIteration().on(ANY).go(L, INIT)

        return END


class GoldMachine(TuringMachine):

    def __init__(self):
        super().__init__(GOLD_ALPHABET, GoldState)
        self.BEGIN.main().end()
