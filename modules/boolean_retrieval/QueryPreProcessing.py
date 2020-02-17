##### CODE ON THIS FILE BASED ON THE FOLLOWING SOURCE #####
# https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html #

class QueryPreProcessing:

    def infixToPostfix(self, prec, infixexpr):
        opStack = []
        postfixList = []
        infixexpr = infixexpr.replace('(', '( ')
        infixexpr = infixexpr.replace(')', ' )')
        tokenList = infixexpr.split()
        
        for token in tokenList:
            if token not in prec and token != ")":
                postfixList.append(token)
            elif token == '(':
                opStack.append(token)
            elif token == ')':
                topToken = opStack.pop()
                while topToken != '(':
                    postfixList.append(topToken)
                    topToken = opStack.pop()
            else:
                while (len(opStack) > 0) and \
                (prec[opStack[-1]] >= prec[token]):
                    postfixList.append(opStack.pop())
                opStack.append(token)

        while (len(opStack) > 0):
            postfixList.append(opStack.pop())
        return " ".join(postfixList)

    def postfixEval(self, func, prec, postfixExpr):
        operandStack = []
        tokenList = postfixExpr.split()
        
        for token in tokenList:
            if token not in prec:
                operandStack.append(token)
            else:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result = func(token,operand1,operand2)
                operandStack.append(result)
        return operandStack.pop()