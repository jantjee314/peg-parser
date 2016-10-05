__author__ = 'jan'

terminals = "abc"
nonterminals = "ABCD"
rules = {
    "A":"(aAb)/E",
    "B":"(bBc)/E",
    "D":"!(!(A!b))a*B!(a/b/c)",
}
FAIL = "failure"
PARSEFAIL= "parse failure"



def match (e, w):
    if e == "E":
        e=""
    if len(e) == 0:
        return (1,"")
    if len(e) == 1 and e[0] in terminals:
        if len(w) > 0 and e == w[0]:
            return (1, e)
        else:
            return (1, FAIL)
    if len(e) == 1 and e[0] in nonterminals:
        rule = rules[e[0]]
        return match(rule + e[1:], w)
    if len(e) > 1:
        # negation
        if e[0] == "!":
            expressions = split(e[1:])
            result = match(expressions[0], w)
            if result[1] != FAIL:
                return (result[0] + 1, FAIL)
            result1 =  match(expressions[1],w)
            return result1[0] + result[0] + 1, result1[1]
        expressions = split(e)
        if len(expressions[1]) == 0:
            return match(expressions[0],w)
        # alternation
        if expressions[1][0] == "/":
            result = match(expressions[0], w)
            if result[1] != FAIL:
                return result
            result2 = match(expressions[1][1:],w)
            return result2[0] + result[0], result2[1]
        # repetitions
        if expressions[1][0] == "*":
            result = match(expressions[0], w)
            if result[1] == FAIL:
                result2 = match(expressions[1][1:], w)
                if result2[1] == FAIL:
                    return result[0] + result2[0] + 1, FAIL
                return result[0] + result2[0] + 1, result2[1]
            result2 = match("(" + expressions[0] + ")" + expressions[1], w.replace(result[1],"", 1))
            if result2[1] == FAIL:
                return (result2[0] + result[0] + 1, FAIL)
            return (result2[0] + result[0] + 1, result[1] + result2[1])
        # concat
        result = match(expressions[0], w)
        if result[1] == FAIL:
            return (result[0] + 1, FAIL)
        w = w.replace(result[1], "",1)
        result2 = match(expressions[1], w)
        if result2[1] == FAIL:
            return (result[0] + result2[0] + 1, FAIL)
        else:
            return (result2[0] + result[0] + 1, result[1] + result2[1])
    if len(w) == 0:
        return (1,FAIL)
    else:
        return (1, PARSEFAIL)



#split expressions
def split(e):
    if e[0] == "(":
        expres1 = ""
        count = 0
        for s in e[1:]:
            if s == "(":
                count +=1
            if count == 0 and s == ")":
                return expres1, e.replace("(" + expres1 + ")","",1)
            if s == ")":
                count -= 1
            expres1 += s
    else:
        return e[0], e[1:]



print(match("(!(!(a*))a)*", "a"))

r = match("(!(!(a*))a)*", "a" * 10)
r2 = match("(!(!(a*))a)*", "a" * 50)
r3 = match("(!(!(a*))a)*", "a" * 100)
print (str(r[0]) + " :: " + str(r2[0]) + " :: " + str(r3[0]))
print(r2[0] / r[0])
print(r3[0] / r2[0])
origin = r[0]



