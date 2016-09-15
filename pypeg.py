__author__ = 'jan'

terminals = "ab"
nonterminals = "A"
rules = {"A":"(aA)/E"}
FAIL = "failure"
PARSEFAIL= "parse failure"



def match (e, w):
    if e == "E":
        e=""
    if len(e) == 0:
        return (1,"")
    if len (w) == 0:
        return (1, FAIL)
    if len(e) == 1 and e[0] in terminals:
        if e == w[0]:
            return (1, e)
        else:
            return (1, FAIL)
    if len(e) == 1 and e[0] in nonterminals:
        rule = rules[e[0]]
        return match(rule + e[1:], w)
    if len(e) > 1:
        expressions = split(e)
        # alternation
        if expressions[1][0] == "/":
            result = match(expressions[0], w)
            if result[1] != FAIL:
                return result
            result2 = match(expressions[1][1:],w)
            return result2[0] + result[0], result2[1]

        result = match(expressions[0], w)
        if result[1] == FAIL:
            return (result[0] + 1, FAIL)
        result2 = match(expressions[1], w.replace(result[1], "",1))
        if result2[1] == FAIL:
            return (result[0] + result2[0] + 1, FAIL)
        else:
            return (result2[0] + result[0] + 1, result[1] + result2[1])
    else:
        return (1, PARSEFAIL)


def split(e):
    if e[0] == "(":
        expres1 = ""
        count = 0
        for s in e[1:]:
            if count == 0 and s == ")":
                return expres1, e.replace("(" + expres1 + ")","",1)
            expres1 += s
    else:
        return e[0], e[1:]



print(match("a/b", "b"))
print(match("A", "aaabaaab"))


