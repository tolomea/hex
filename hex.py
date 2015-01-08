from __future__ import division

import string
from itertools import chain
from collections import defaultdict
import sys
import json

rows = [
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
]
cols = [
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
]
diags = [
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
]
edges = [rows, cols, diags]

answer = {
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
}

def get_char(e, chars):
    if e and e[0] in chars:
        return e.pop(0)
    else:
        return None


LETTERS = string.ascii_uppercase
DIGITS = string.digits


class OrChain(object):
    def __init__(self, e):
        self.options = [ExpressionList(e)]
        while get_char(e, "|"):
            self.options.append(ExpressionList(e))

    def __str__(self):
        return "|".join(str(o) for o in self.options)

    def match(self, used, remaining, context):
        index = len(context)
        context.append(None)

        for option in self.options:
            for new_used, new_context in option.match(used, remaining, context):
                context[index] = len(used), len(new_used)
                yield new_used, new_context

        assert len(context) == index + 1
        context.pop()


class ExpressionList(object):
    def __init__(self, e):
        self.exps = [ModifierExpression(e)]
        while e and e[0] in "[(\\." + LETTERS:
            self.exps.append(ModifierExpression(e))

    def __str__(self):
        return "".join(str(o) for o in self.exps)

    def match(self, used, remaining, context):
        def recurse(used, remaining, context, exps):
            if exps:
                for partial_used, partial_context in exps[0].match(used, remaining, context):
                    partial_remaining = remaining[len(partial_used)-len(used):]
                    for new_used, new_context in recurse(partial_used, partial_remaining, partial_context, exps[1:]):
                        yield new_used, new_context
            else:
                yield used, context

        for new_used, new_context in recurse(used, remaining, context, self.exps):
            yield new_used, new_context


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

    def match(self, used, remaining, context):
        def recurse(used, remaining, context):
            for partial_used, partial_context in self.expression.match(used, remaining, context):
                if len(partial_used) > len(used):
                    yield partial_used, partial_context
                    partial_remaining = remaining[len(partial_used)-len(used):]
                    for new_used, new_context in recurse(partial_used, partial_remaining, partial_context):
                        yield new_used, new_context

        if self.modifier in list("?*"):
            yield used, context

        if self.modifier in list("+*"):
            for new_used, new_context in recurse(used, remaining, context):
                yield new_used, new_context
        else:
            for new_used, new_context in self.expression.match(used, remaining, context):
                yield new_used, new_context


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
        # hack around \n expressions for now by treating them as .*
        res = ClassExpression(e)
    elif get_char(e, "."):
        res = Letters(LETTERS)
    else:
        c = get_char(e, LETTERS)
        assert c
        res = Letters(c)
    return res


class ClassExpression(object):
    def __init__(self, e):
        self.group = int(get_char(e, DIGITS))
        assert self.group

    def __str__(self):
        return "\\" + str(self.group)

    def match(self, used, remaining, context):
        s,e = context[self.group]
        consume = [o & n for o, n in zip(used[s:e], remaining)]
        if all(consume) and len(consume) == e-s:
            yield used[:s] + consume + used[e:] + consume, context


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

    def match(self, used, remaining, context):
        if remaining:
            hits = remaining[0] & self.options
            if hits:
                yield used + [hits], context


def parse(regexp_str):
    l = list(regexp_str)
    res = OrChain(l)
    assert not l, l
    return res


def match(regexp, char_list):
    new_char_lists = []
    for new_char_list, new_context in regexp.match([], char_list, []):
        if len(new_char_list) == len(char_list):
            new_char_lists.append(new_char_list)
    assert new_char_lists
    new_char_list = [set(chain(*x)) for x in zip(*new_char_lists)]
    return new_char_list


class HexGrid(object):
    def __init__(self, rows, cols, diags):
        size = len(rows)
        assert len(cols) == size
        assert len(diags) == size
        hang = size // 2
        self.size = size
        self.hang = hang

        # line is a tuple of the regex and the list of cell locations
        self.lines = []

        # maps cell indicies to line indicies
        self.cell_lines = defaultdict(set)

        # cell is a set of possible values for that location
        # indexed by (row, col)
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


def solve(edges):
    # check the grid is symettric
    grid = HexGrid(
        [parse(e) for e in rows],
        [parse(e) for e in cols],
        [parse(e) for e in diags],
    )

    queue = set(range(len(grid.lines)))

    while queue:
        line_id = queue.pop()
        regex, cell_ids = grid.lines[line_id]
        cells = [grid.cells[cell_id] for cell_id in cell_ids]
        new_cells = match(regex, cells)
        for i, o, n in zip(cell_ids, cells, new_cells):
            if n != o:
                grid.cells[i] = n
                queue.update(grid.cell_lines[i])
                queue.remove(line_id)
    grid.dump()

    assert {k: "".join(v) for k, v in grid.cells.iteritems()} == answer


if __name__ == "__main__":
    c = [set("ABC"), set("ABC"), set("ABC")]
    x = match(parse(".*"), c)
    assert x == [set("ABC"), set("ABC"), set("ABC")], x

    c = [set("BC"), set("AC"), set("AB")]
    assert match(parse(".*"), c) == [set("BC"), set("AC"), set("AB")]
    assert match(parse("[AB]*"), c) == [set("B"), set("A"), set("AB")]
    assert match(parse("(A|B)*"), c) == [set("B"), set("A"), set("AB")]
    assert match(parse("(A|B)*B"), c) == [set("B"), set("A"), set("B")]
    assert match(parse("....?"), c) == [set("BC"), set("AC"), set("AB")]
    assert match(parse("(.*)*"), c) == [set("BC"), set("AC"), set("AB")]
    assert match(parse(".*.*"), c) == [set("BC"), set("AC"), set("AB")]

    solve(edges)


