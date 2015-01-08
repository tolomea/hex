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

loop_puzzle3 = {
    "rows": [
        r".X",
        r"(AA|BB|CC)X",
        r"XX",
    ],
    "cols": [
        r"CC|AB|BA",
        r"X.X",
        r"XX",
    ],
    "diags": [
        r"X.",
        r"X(AA|BB|CC)",
        r"XX",
    ],
    "answer": {
        (0, 0): "C",
        (0, 1): "C",
        (1, 0): "X",
        (1, 1): "C",
        (1, 2): "X",
        (2, 1): "X",
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


LETTERS = string.ascii_uppercase
DIGITS = string.digits


def get_char(e, chars):
    if e and e[0] in chars:
        return e.pop(0)
    else:
        return None


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
                yield MatchState(self.remaining[1:], self.done + (hits,), self.groups)

    def start_group(self):
        groups = self.groups + (None,)
        return MatchState(self.remaining, self.done, groups)

    def end_group(self, old_state):
        # old_state must be the state returned by create_group
        groups = list(self.groups)
        group_idx = len(old_state.groups) - 1
        assert groups[group_idx] is None
        groups[group_idx] = (len(old_state.done), len(self.done))
        return MatchState(self.remaining, self.done, groups)

    def consume_group(self, index):
        start, end = self.groups[index]
        consume = tuple(o & n for o, n in zip(self.done[start:end], self.remaining))
        if all(consume) and len(consume) == end - start:
            remaining = self.remaining[len(consume):]
            done = self.done[:start] + consume + self.done[end:] + consume
            return MatchState(remaining, done, self.groups)


class Matcher(object):
    def __init__(self, regex_str):
        l = list(regex_str)
        self.exp = OrChain(l)
        assert not l, l  # check we consumed the whole string

    def match(self, target):
        matches = [[set() for x in target]]
        for match in self.exp.match(MatchState(target)):
            if not match.remaining:
                matches.append(match.done)
        return [set(chain(*x)) for x in zip(*matches)]


class OrChain(object):
    def __init__(self, e):
        self.options = [ExpressionList(e)]
        while get_char(e, "|"):
            self.options.append(ExpressionList(e))

    def __str__(self):
        return "|".join(str(o) for o in self.options)

    def match(self, state):
        state = state.start_group()
        for option in self.options:
            for new_state in option.match(state):
                yield new_state.end_group(state)


class ExpressionList(object):
    def __init__(self, e):
        self.expressions = [ModifierExpression(e)]
        while e and e[0] in "[(\\." + LETTERS:
            self.expressions.append(ModifierExpression(e))

    def __str__(self):
        return "".join(str(o) for o in self.exps)

    def match(self, state):
        def recurse(state, expressions):
            if expressions:
                for partial_state in expressions[0].match(state):
                    for new_state in recurse(partial_state, expressions[1:]):
                        yield new_state
            else:
                yield state

        for new_state in recurse(state, self.expressions):
            yield new_state


class ModifierExpression(object):
    def __init__(self, e):
        self.expression = BasicExpression(e)
        self.modifier = get_char(e, "*+?")

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
        res = CharacterClass(letters)
    elif get_char(e, "("):
        res = OrChain(e)
        assert get_char(e, ")")
    elif get_char(e, "\\"):
        res = BackReference(e)
    elif get_char(e, "."):
        res = CharacterClass(LETTERS)
    else:
        c = get_char(e, LETTERS)
        assert c
        res = CharacterClass(c)
    return res


class BackReference(object):
    def __init__(self, e):
        self.group = int(get_char(e, DIGITS))
        assert self.group

    def __str__(self):
        return "\\" + str(self.group)

    def match(self, state):
        new_state = state.consume_group(self.group)
        if new_state:
            yield new_state


class CharacterClass(object):
    def __init__(self, options):
        self.options = set(options)

    def __str__(self):
        if len(self.options) == 1:
            res, = self.options
            return res
        elif self.options == set(LETTERS):
            return "."
        elif len(self.options) > 13:
            return "[^" + "".join(sorted(set(LETTERS) - self.options)) + "]"
        else:
            return "[" + "".join(sorted(self.options)) + "]"

    def match(self, state):
        for new_state in state.consume(self.options):
            yield new_state


class Grid(object):
    def __init__(self, size):
        hang = size // 2
        self.size = size
        self.hang = hang

        # line is a list of cell locations
        # [[cell_index...]...]
        self.lines = []

        # maps cell indicies to a set of line indicies
        # {cell_index: {line_index...}}
        self.cell_lines = defaultdict(set)

        # cell is a set of possible values for that location indexed by (row, col)
        # {(row, col): {possible_value...}}
        self.cells = {}

        # rows
        for y in range(size):
            cell_ids = []
            for x in range(max(0, y-hang), min(size, y+hang+1)):
                cell_ids.append((x, y))
            self.lines.append(cell_ids)

        # cols
        for x in range(size):
            cell_ids = []
            for y in range(max(0, x-hang), min(size, x+hang+1)):
                cell_ids.append((x, y))
            self.lines.append(cell_ids)

        # diags
        for i in range(size):
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
            self.lines.append(cell_ids)

        # cells and cell_lines
        for line_id, cells in enumerate(self.lines):
            for cell_id in cells:
                self.cells[cell_id] = set(LETTERS)
                self.cell_lines[cell_id].add(line_id)

    def copy(self):
        new = copy.copy(self)
        new.cells = copy.deepcopy(self.cells)
        return new

    def solved(self):
        return all(len(c) == 1 for c in self.cells.values())

    def valid(self):
        return all(c for c in self.cells.values())

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


def propagate(grid, matchers):
    queue = set(range(len(grid.lines)))
    while queue:
        line_id = queue.pop()
        cell_ids = grid.lines[line_id]
        old_cells = [grid.cells[cell_id] for cell_id in cell_ids]
        new_cells = matchers[line_id].match(old_cells)
        for cell_id, old_cell, new_cell in zip(cell_ids, old_cells, new_cells):
            if old_cell != new_cell:
                grid.cells[cell_id] = new_cell
                queue.update(grid.cell_lines[cell_id])


def search(grid, matchers):
    propagate(grid, matchers)
    if grid.valid():
        if grid.solved():
            yield grid
        else:
            for cell_id, cell in grid.cells.iteritems():
                if len(cell) > 1:
                    for value in cell:
                        new_state = grid.copy()
                        new_state.cells[cell_id] = {value}
                        for x in search(new_state, matchers):
                            yield x
                    break


if __name__ == "__main__":
    def solve(puzzle):
        matchers = []
        matchers.extend(Matcher(e) for e in puzzle["rows"])
        matchers.extend(Matcher(e) for e in puzzle["cols"])
        matchers.extend(Matcher(e) for e in puzzle["diags"])

        print "-" * 20
        grid = Grid(len(puzzle["rows"]))
        for grid in search(grid, matchers):
            grid.dump()
            print
        assert {k: "".join(v) for k, v in grid.cells.iteritems()} == puzzle["answer"]

    c = [set("ABC"), set("ABC"), set("ABC")]
    x = Matcher(".*").match(c)
    assert x == [set("ABC"), set("ABC"), set("ABC")], x

    c = [set("BC"), set("AC"), set("AB")]
    assert Matcher(".*").match(c) == [set("BC"), set("AC"), set("AB")]
    assert Matcher("[AB]*").match(c) == [set("B"), set("A"), set("AB")]
    assert Matcher("(A|B)*").match(c) == [set("B"), set("A"), set("AB")]
    assert Matcher("(A|B)*B").match(c) == [set("B"), set("A"), set("B")]
    assert Matcher("....?").match(c) == [set("BC"), set("AC"), set("AB")]
    assert Matcher("(.*)*").match(c) == [set("BC"), set("AC"), set("AB")]
    assert Matcher(".*.*").match(c) == [set("BC"), set("AC"), set("AB")]
    c = [set("C"), set("A"), set("A")]
    assert Matcher(r"(.)\1\1").match(c) == [set(), set(), set()]

    solve(original_puzzle)
    solve(group_puzzle)
    solve(nothing_puzzle)
    solve(loop_puzzle)
    solve(loop_puzzle2)
    solve(loop_puzzle3)
