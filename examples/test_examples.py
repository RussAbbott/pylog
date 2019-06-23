import pytest
from pylog.logic_variables import PyValue

class TestClass(object):

    def test_cryptarithmetic(self):
        import cryptarithmetic
        t1, t2, s, _Z, Blank = 'SEND', 'MORE', 'MONEY', PyValue(0), PyValue(' ')
        (Carries, T1, T2, Sum, Leading_Digits) = cryptarithmetic.set_up_puzzle(t1, t2, s, _Z)
        next(cryptarithmetic.solve(Carries, T1, T2, Sum, Leading_Digits))
        (t1_out, t2_out, tot_out) = (cryptarithmetic.solution_to_string(T, _Z, Blank) for T in [T1[1:], T2[1:], Sum[1:]])
        assert (t1_out, t2_out, tot_out) == (' 9567', ' 1085', '10652')

        