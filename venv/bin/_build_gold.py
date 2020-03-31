from gold import GoldMachine

import compiler


machine = GoldMachine()
machine.TAPE = '. E E 1 1 T t S . . . . . . N 1 * 1 1 E'


result = compiler.compile_dtm(machine, 'out/gold.dtm', blank='.')
result = compiler.compile_turing(machine, 'out/gold.utm')
