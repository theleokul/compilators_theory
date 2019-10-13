stack = '#'
pol_not = ''
steps = []
all_ops = ['+', '-', '*', '/', ')', '#', ',', '>', '<', '^']


class Grammatic:
    def __init__(self, rule, pol_not, cond, proc):
        self.rule = rule  # ('E', 'E+T')
        self.pol_not = pol_not  # 'ET+'
        self.cond = cond  # ('+', '-', '#')
        self.proc = proc  # '+'

    def process_sdt(self, seq, seq_i: int, gram_i: int):
        global stack
        global pol_not
        global steps

        # a - is an abstract terminal, so we should replace it with an actual terminal from stack
        rule_1 = self.rule[1]
        if stack[-1].islower() and rule_1 == 'a':
            rule_1 = stack[-1]

        proc = self.proc
        if stack[-1].islower() and proc == 'a':
            proc = stack[-1]

        cur_let = seq[seq_i]

        if stack.endswith(rule_1) and cur_let in self.cond:
            pol_not += proc
            steps.append([stack, cur_let, seq[seq_i+1:], str(gram_i + 1), pol_not])
            stack = stack[:-len(rule_1)] + self.rule[0]
            return True
        return False


grams = [
    # < - actually <<. There is some limitations, because I read sequence by one 1 char at a time
    Grammatic(rule=('M', 'M<E'), pol_not='ME<', cond=[op for op in all_ops if op not in ('*', '/', '^', '+', '-')], proc='<'),
    Grammatic(rule=('M', 'M>E'), pol_not='ME>', cond=[op for op in all_ops if op not in ('*', '/', '^', '+', '-')], proc='>'),
    Grammatic(rule=('M', 'E'), pol_not='E', cond=[op for op in all_ops if op not in ('*', '/', '^', '+', '-')], proc=''),
    Grammatic(rule=('E', 'E+T'), pol_not='ET+', cond=[op for op in all_ops if op not in ('*', '/', '^')], proc='+'),
    Grammatic(rule=('E', 'E-T'), pol_not='ET+', cond=[op for op in all_ops if op not in ('*', '/', '^')], proc='-'),
    Grammatic(rule=('E', 'T'), pol_not='T', cond=[op for op in all_ops if op not in ('*', '/', '^')], proc=''),
    Grammatic(rule=('T', 'T*F'), pol_not='TF*', cond=[op for op in all_ops if op not in ('^')], proc='*'),
    Grammatic(rule=('T', 'T/F'), pol_not='TF/', cond=[op for op in all_ops if op not in ('^')], proc='/'),
    Grammatic(rule=('T', 'F'), pol_not='F', cond=[op for op in all_ops if op not in ('^')], proc=''),
    Grammatic(rule=('F', 'F^P'), pol_not='FP^', cond=all_ops[:], proc='^'),
    Grammatic(rule=('F', 'P'), pol_not='P', cond=all_ops[:], proc=''),
    Grammatic(rule=('P', 'f()'), pol_not='', cond=all_ops[:], proc='[F ARGS 0]'),
    Grammatic(rule=('P', 'f(M)'), pol_not='', cond=all_ops[:], proc='[F ARGS 1]'),  # F - represents specific function
    Grammatic(rule=('P', 'f(M,M)'), pol_not='', cond=all_ops[:], proc='[F ARGS 2]'),
    Grammatic(rule=('P', 'f(M,M,M)'), pol_not='', cond=all_ops[:], proc='[F ARGS 3]'),
    Grammatic(rule=('P', 'sin(M)'), pol_not='', cond=all_ops[:], proc='[SIN]'),  # S - represents sinus
    Grammatic(rule=('P', '-E'), pol_not='', cond=all_ops[:], proc='[UNARY MINUS]'),  # _ - represents unary minus
    Grammatic(rule=('P', 'a'), pol_not='a', cond=all_ops[:], proc='a'),
    Grammatic(rule=('P', '(M)'), pol_not='', cond=all_ops[:], proc='')
]
