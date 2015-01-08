from __future__ import division

import string
from itertools import chain
from collections import defaultdict, namedtuple
import sys
import copy


original_puzzle = {
    "rows": [
        r".*H.*H.*",
        r"(DI|NS|TH|OM)*",
        r"F.*[AO].*[AO].*",
        r"(O|RHH|MM)*",
        r".*",
        r"C*MC(CCC|MM)*",
        r"[^C]*[^R]*III.*",
        r"(...?)\1*",
        r"([^X]|XCC)*",
        r"(RR|HHH)*.?",
        r"N.*X.X.X.*E",
        r"R*D*M*",
        r".(C|HH)*",
    ],
    "cols": [
        r"(ND|ET|IN)[^X]*",
        r"[CHMNOR]*I[CHMNOR]*",
        r"P+(..)\1.*",
        r"(E|CR|MN)*",
        r"([^MC]|MM|CC)*",
        r"[AM]*CM(RC)*R?",
        r".*",
        r".*PRR.*DDC.*",
        r"(HHX|[^HX])*",
        r"([^EMC]|EM)*",
        r".*OXR.*",
        r".*LR.*RL.*",
        r".*SE.*UE.*",
    ],
    "diags": [
        r".*G.*V.*H.*",
        r"[CR]*",
        r".*XEXM*",
        r".*DD.*CCM.*",
        r".*XHCR.*X.*",
        r".*(.)(.)(.)(.)\4\3\2\1.*",
        r".*(IN|SE|HI)",
        r"[^C]*MMM[^C]*",
        r".*(.)C\1X\1.*",
        r"[CEIMU]*OH[AEMOR]*",
        r"(RX|[^R])*",
        r"[^M]*M[^M]*",
        r"(S|MM|HHH)*",
    ],
    "answer": {
        (0, 0): "N",
        (0, 1): "D",
        (0, 2): "F",
        (0, 3): "M",
        (0, 4): "M",
        (0, 5): "C",
        (0, 6): "H",
        (1, 0): "H",
        (1, 1): "I",
        (1, 2): "O",
        (1, 3): "M",
        (1, 4): "C",
        (1, 5): "M",
        (1, 6): "R",
        (1, 7): "O",
        (2, 0): "P",
        (2, 1): "O",
        (2, 2): "X",
        (2, 3): "O",
        (2, 4): "X",
        (2, 5): "C",
        (2, 6): "X",
        (2, 7): "R",
        (2, 8): "V",
        (3, 0): "E",
        (3, 1): "M",
        (3, 2): "N",
        (3, 3): "M",
        (3, 4): "N",
        (3, 5): "C",
        (3, 6): "R",
        (3, 7): "E",
        (3, 8): "C",
        (3, 9): "R",
        (4, 0): "H",
        (4, 1): "O",
        (4, 2): "X",
        (4, 3): "M",
        (4, 4): "M",
        (4, 5): "C",
        (4, 6): "C",
        (4, 7): "O",
        (4, 8): "X",
        (4, 9): "R",
        (4, 10): "N",
        (5, 0): "A",
        (5, 1): "M",
        (5, 2): "A",
        (5, 3): "M",
        (5, 4): "M",
        (5, 5): "C",
        (5, 6): "M",
        (5, 7): "R",
        (5, 8): "C",
        (5, 9): "R",
        (5, 10): "C",
        (5, 11): "R",
        (6, 0): "S",
        (6, 1): "T",
        (6, 2): "X",
        (6, 3): "M",
        (6, 4): "C",
        (6, 5): "M",
        (6, 6): "I",
        (6, 7): "E",
        (6, 8): "C",
        (6, 9): "R",
        (6, 10): "X",
        (6, 11): "R",
        (6, 12): "G",
        (7, 1): "H",
        (7, 2): "P",
        (7, 3): "R",
        (7, 4): "R",
        (7, 5): "M",
        (7, 6): "I",
        (7, 7): "O",
        (7, 8): "H",
        (7, 9): "H",
        (7, 10): "D",
        (7, 11): "D",
        (7, 12): "C",
        (8, 2): "H",
        (8, 3): "H",
        (8, 4): "X",
        (8, 5): "M",
        (8, 6): "I",
        (8, 7): "R",
        (8, 8): "H",
        (8, 9): "H",
        (8, 10): "X",
        (8, 11): "D",
        (8, 12): "C",
        (9, 3): "H",
        (9, 4): "E",
        (9, 5): "M",
        (9, 6): "H",
        (9, 7): "E",
        (9, 8): "M",
        (9, 9): "H",
        (9, 10): "E",
        (9, 11): "M",
        (9, 12): "H",
        (10, 4): "M",
        (10, 5): "M",
        (10, 6): "X",
        (10, 7): "O",
        (10, 8): "X",
        (10, 9): "R",
        (10, 10): "X",
        (10, 11): "M",
        (10, 12): "H",
        (11, 5): "M",
        (11, 6): "L",
        (11, 7): "R",
        (11, 8): "C",
        (11, 9): "R",
        (11, 10): "L",
        (11, 11): "M",
        (11, 12): "C",
        (12, 6): "S",
        (12, 7): "E",
        (12, 8): "C",
        (12, 9): "U",
        (12, 10): "E",
        (12, 11): "M",
        (12, 12): "C",
    },
}

loop_puzzle = {
    "rows": [
        r".X",
        r"(.)\1\1",
        r"XX",
    ],
    "cols": [
        r"BA|AC|BB",
        r".*",
        r".*",
    ],
    "diags": [
        r".*",
        r".(CB|AA|AB)",
        r".*",
    ],
    "answer": {
        (0, 0): "B",
        (0, 1): "A",
        (1, 0): "X",
        (1, 1): "A",
        (1, 2): "X",
        (2, 1): "A",
        (2, 2): "X",
    },
}

loop_puzzle2 = {
    "rows": [
        r".X",
        r"(.)\1\1",
        r"XX",
    ],
    "cols": [
        r"CC|AB|BA",
        r".*",
        r".*",
    ],
    "diags": [
        r".*",
        r".(CC|AA|BB)",
        r".*",
    ],
    "answer": {
        (0, 0): "C",
        (0, 1): "C",
        (1, 0): "X",
        (1, 1): "C",
        (1, 2): "X",
        (2, 1): "C",
        (2, 2): "X",
    },
}

group_puzzle = {
    "rows": [
        r"XX",
        r"(.)\1\1",
        r"XX",
    ],
    "cols": [
        r"X[ABC]",
        r"X[AB]X",
        r"[AC]X",
    ],
    "diags": [
        r".*",
        r".*",
        r".*",
    ],
    "answer": {
        (0, 0): "X",
        (0, 1): "A",
        (1, 0): "X",
        (1, 1): "A",
        (1, 2): "X",
        (2, 1): "A",
        (2, 2): "X",
    },
}

nothing_puzzle = {
    "rows": [
        r"(.*)*X",
    ],
    "cols": [
        r"(.?)+X",
    ],
    "diags": [
        r"(.*)\1X",
    ],
    "answer": {
        (0, 0): "X",
    },
}


class Regex(object):
    def __init__(self, regex_str):
        l = list(regex_str)
        self.exp = OrChain(l)
        assert not l, l

    def match(self, target):
        result = [[set() for x in target]]
        for state in self.exp.match(MatchState(target)):
            if not state.remaining:
                result.append(state.done)
        return [set(chain(*x)) for x in zip(*result)]


def get_char(e, chars):
    if e and e[0] in chars:
        return e.pop(0)
    else:
        return None


LETTERS = string.ascii_uppercase
DIGITS = string.digits


class MatchState(namedtuple("MatchState", "remaining done groups")): # really seriously immutable
    __slots__ = ()

    def __new__(cls, remaining, done=(), groups=()):
        remaining = tuple(remaining)
        done = tuple(done)
        groups = tuple(groups)
        return super(MatchState, cls).__new__(cls, remaining, done, groups)

    def consume(self, chars):
        if self.remaining:
            hits = self.remaining[0] & chars
            if hits:
                return MatchState(self.remaining[1:], self.done + (hits,), self.groups)
        return None

    def create_group(self):
        groups = self.groups + (None,)
        return MatchState(self.remaining, self.done, groups)

    def set_group(self, old_state):
        # old_state must be the state returned by create_group
        groups = list(self.groups)
        groups[len(old_state.groups) - 1] = (len(old_state.done), len(self.done))
        return MatchState(self.remaining, self.done, groups)

    def consume_group(self, index):
        s,e = self.groups[index]
        consume = tuple(o & n for o, n in zip(self.done[s:e], self.remaining))
        if all(consume) and len(consume) == e-s:
            remaining = self.remaining[len(consume):]
            done = self.done[:s] + consume + self.done[e:] + consume
            return MatchState(remaining, done, self.groups)


class OrChain(object):
    def __init__(self, e):
        self.options = [ExpressionList(e)]
        while get_char(e, "|"):
            self.options.append(ExpressionList(e))

    def __str__(self):
        return "|".join(str(o) for o in self.options)

    def match(self, state):
        state = state.create_group()

        for option in self.options:
            for new_state in option.match(state):
                yield new_state.set_group(state)


class ExpressionList(object):
    def __init__(self, e):
        self.exps = [ModifierExpression(e)]
        while e and e[0] in "[(\\." + LETTERS:
            self.exps.append(ModifierExpression(e))

    def __str__(self):
        return "".join(str(o) for o in self.exps)

    def match(self, state):
        def recurse(state, exps):
            if exps:
                for partial_state in exps[0].match(state):
                    for new_state in recurse(partial_state, exps[1:]):
                        yield new_state
            else:
                yield state

        for new_state in recurse(state, self.exps):
            yield new_state


class ModifierExpression(object):
    def __init__(self, e):
        self.expression = BasicExpression(e)
        if e and e[0] in "*+?":
            self.modifier = e.pop(0)
        else:
            self.modifier = None

    def __str__(self):
        res = str(self.expression)
        if isinstance(self.expression, OrChain):
            res = "(" + res + ")"
        if self.modifier:
            res += self.modifier
        return res

    def match(self, state):
        def recurse(state):
            for partial_state in self.expression.match(state):
                yield partial_state
                if len(partial_state.done) > len(state.done):
                    for new_state in recurse(partial_state):
                        yield new_state

        if self.modifier in list("?*"):
            yield state

        if self.modifier in list("+*"):
            for new_state in recurse(state):
                yield new_state
        else:
            for new_state in self.expression.match(state):
                yield new_state


def BasicExpression(e):
    if get_char(e,"["):
        negate = get_char(e, "^")
        letters = set()
        l = get_char(e, LETTERS)
        while l:
            letters.add(l)
            l = get_char(e, LETTERS)
        if negate:
            letters = set(LETTERS) - letters
        assert get_char(e, "]")
        return Letters(letters)
    elif get_char(e, "("):
        res = OrChain(e)
        assert get_char(e, ")")
    elif get_char(e, "\\"):
        res = ReferenceExpression(e)
    elif get_char(e, "."):
        res = Letters(LETTERS)
    else:
        c = get_char(e, LETTERS)
        assert c
        res = Letters(c)
    return res


class ReferenceExpression(object):
    def __init__(self, e):
        self.group = int(get_char(e, DIGITS))
        assert self.group

    def __str__(self):
        return "\\" + str(self.group)

    def match(self, state):
        new_state = state.consume_group(self.group)
        if new_state:
            yield new_state


class Letters(object):
    def __init__(self, options):
        self.options = set(options)

    def __str__(self):
        if len(self.options) == 1:
            return list(self.options)[0]
        elif self.options == set(LETTERS):
            return "."
        elif len(self.options) > 13:
            return "[^" + "".join(sorted(set(LETTERS) - self.options)) + "]"
        else:
            return "[" + "".join(sorted(self.options)) + "]"

    def match(self, state):
        new_state = state.consume(self.options)
        if new_state:
            yield new_state


class State(object):
    def get_all_constraints(self):
        # return all the constraints
        pass

    def evaluate(self, constraint):
        # evaluate the given constraint, update this stat in place return a list of constraints that may need checking
        pass

    def copy(self):
        # return a full copy of this state
        pass

    def solved(self):
        # return true if this is a solved state
        pass

    def valid(self):
        # return true if the state is valid
        pass


class HexPuzzle(State):
    def __init__(self, puzzle):
        rows = [Regex(e) for e in puzzle["rows"]]
        cols = [Regex(e) for e in puzzle["cols"]]
        diags = [Regex(e) for e in puzzle["diags"]]

        size = len(rows)
        assert len(cols) == size
        assert len(diags) == size
        hang = size // 2
        self.size = size
        self.hang = hang

        # line is a tuple of the regex and the list of cell locations
        # [(regex, [cell_index...])...]
        self.lines = []

        # maps cell indicies to a set of line indicies
        # {cell_index: {line_index...}}
        self.cell_lines = defaultdict(set)

        # cell is a set of possible values for that location indexed by (row, col)
        # {(row, col): {possible_value...}}
        self.cells = {}

        # rows
        for y, regex in enumerate(rows):
            cell_ids = []
            for x in range(max(0, y-hang), min(size, y+hang+1)):
                cell_ids.append((x, y))
            self.lines.append((regex, cell_ids))

        # cols
        for x, regex in enumerate(cols):
            cell_ids = []
            for y in range(max(0, x-hang), min(size, x+hang+1)):
                cell_ids.append((x, y))
            self.lines.append((regex, cell_ids))

        # diags
        for i, regex in enumerate(diags):
            cell_ids = []
            if i < hang:
                length = size - hang + i
                start_x = length - 1
                start_y = size - 1
            else:
                length = size + hang - i
                start_x = size - 1
                start_y =  length - 1
            for j in range(length):
                cell_ids.append((start_x - j, start_y - j))
            self.lines.append((regex, cell_ids))

        # cells and cell_lines
        for line_id, (regex, cells) in enumerate(self.lines):
            for cell_id in cells:
                self.cells[cell_id] = set(LETTERS)
                self.cell_lines[cell_id].add(line_id)

    def dump(self):
        for y in range(self.size):
            if y < self.hang:
                indent = self.hang - y
                start = 0
            else:
                indent = y - self.hang
                start = y - self.hang
            sys.stdout.write(" " * indent * 2)
            for x in range(start, self.size):
                if (x, y) in self.cells:
                    c = self.cells[(x, y)]
                    l = len(c)
                    if l > 1:
                        sys.stdout.write("%02d"%l)
                    elif l == 1:
                        sys.stdout.write("-%s"%list(c)[0])
                    else:
                        sys.stdout.write("XX")
                else:
                    sys.stdout.write("  ")
                sys.stdout.write("  ")
            sys.stdout.write("\n")

    def get_all_constraints(self):
        return range(len(self.lines))

    def evaluate(self, line_id):
        regex, cell_ids = self.lines[line_id]
        cells = [self.cells[cell_id] for cell_id in cell_ids]
        new_cells = regex.match(cells)
        for i, o, n in zip(cell_ids, cells, new_cells):
            if n != o:
                self.cells[i] = n
                for x in self.cell_lines[i]:
                    yield x

    def copy(self):
        new = copy.copy(self)
        new.cells = copy.deepcopy(self.cells)
        return new

    def solved(self):
        return all(len(c) == 1 for c in self.cells.values())

    def valid(self):
        return all(len(c) for c in self.cells.values())

    def get_sub_states(self):
        for k, v in self.cells.iteritems():
            if len(v) > 1:
                for choosen_v in v:
                    new = self.copy()
                    new.cells[k] = {choosen_v}
                    yield new
                break

    def __eq__(self, other):
        return hash(self.key()) == hash(other.key())

    def __hash__(self):
        return hash(self.key())

    def key(self):
        return tuple(frozenset(x) for x in self.cells)

def propagate(state):
    queue = set(state.get_all_constraints())
    while queue:
        constraint = queue.pop()
        queue.update(state.evaluate(constraint))


def constraint_prop_inner(initial_state):
    state = initial_state.copy()
    propagate(state)
    if state.valid():
        if state.solved():
            yield state
        else:
            for sub_state in state.get_sub_states():
                for x in constraint_prop_inner(sub_state):
                    yield x


def constraint_prop(initial_state):
    solutions = set()
    for x in constraint_prop_inner(initial_state):
        if x not in solutions:
            solutions.add(x)
            yield x


if __name__ == "__main__":
    def solve(puzzle):
        print "-" * 20
        hp = HexPuzzle(puzzle)
        #hp, = constraint_prop(hp)
        for hp in constraint_prop(hp):
            hp.dump()

            hp2 = hp.copy()
            propagate(hp2)
            assert hp == hp2
            assert hp2.valid()
            assert hp2.solved()

            print
        assert {k: "".join(v) for k, v in hp.cells.iteritems()} == puzzle["answer"]

    c = [set("ABC"), set("ABC"), set("ABC")]
    x = Regex(".*").match(c)
    assert x == [set("ABC"), set("ABC"), set("ABC")], x

    c = [set("BC"), set("AC"), set("AB")]
    assert Regex(".*").match(c) == [set("BC"), set("AC"), set("AB")]
    assert Regex("[AB]*").match(c) == [set("B"), set("A"), set("AB")]
    assert Regex("(A|B)*").match(c) == [set("B"), set("A"), set("AB")]
    assert Regex("(A|B)*B").match(c) == [set("B"), set("A"), set("B")]
    assert Regex("....?").match(c) == [set("BC"), set("AC"), set("AB")]
    assert Regex("(.*)*").match(c) == [set("BC"), set("AC"), set("AB")]
    assert Regex(".*.*").match(c) == [set("BC"), set("AC"), set("AB")]
    c = [set("C"), set("A"), set("A")]
    assert Regex(r"(.)\1\1").match(c) == [set(), set(), set()]

    solve(original_puzzle)
    solve(group_puzzle)
    solve(nothing_puzzle)
    solve(loop_puzzle)
    solve(loop_puzzle2)


"""
  A B C
 D E F G
H I J K L
 M N O P
  Q R S

A B C
D E F G
H I J K L
  M N O P
    Q R S
"""
