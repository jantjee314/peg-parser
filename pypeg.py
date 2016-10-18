__author__ = 'jan'

terminals = "abc"
nonterminals = "ZT"
rules = {
    "T":"a/b/c",
    "Z":"TZ/E", 
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

expression = raw_input("enter expression:")
print(match("Z", str(expression)))
print(match("((a(Z/E))/E)bb*", str(expression)))
print(match("!abb*", str(expression)))


