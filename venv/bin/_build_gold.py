from gold import GoldMachine

import compiler


machine = GoldMachine()
machine.TAPE = '. S 9 9 9 9 * 9 S'


result = compiler.compile_dtm(machine, 'out/gold.dtm', blank='.')
result = compiler.compile_turing(machine, 'out/gold.utm')
