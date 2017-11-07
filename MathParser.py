import re
import math

class MathParser:
    def __init__(self):
        self.varList = {}
        self.setValue('pi', math.pi)

    def setValue(self, name, value):
        self.varList[str(name)] = float(value)

    def getValue(self, name):
        if not self.varList.get(str(name)) == None:
            return self.varList[str(name)]

    def delValue(self, name):
        if not self.varList.get(name) == None:
            del self.varList[str(name)]

    def _nextToken(self):
        self.prev = self.p

        while (self.p < len(self.expr)) and (self.expr[self.p] == ' '):
            self.p += 1

        s = self.expr[self.p:]

        # number
        r = re.match(r'^[\d]+($|[\.][\d]+|([\.][\d]+[Ee]|[Ee])[+-]?\d+)?', s)

        if r:
            self.p += len(r.group())
            self.token = 'number'
            self.value = r.group()
            return

        # operator
        r = re.match(r'^([+\/\*]|(-(?!>)))', s)

        if r:
            self.p += len(r.group())
            self.token = 'operator' + r.group()
            return

            # ->
        r = re.match(r'^->', s)

        if r:
            self.p += len(r.group())
            token = '->'
            return

            # vars
        r = re.match(r'^[a-zA-Z]+[0-9]*', s)

        if r:
            self.p += len(r.group())
            self.token = 'var'
            self.value = r.group()
            return

            # end
        if s == '':
            self.token = 'end'
            return

        # fail
        raise ValueError('Unexpected symbol!')

    def _calcAll(self):
        if self.token == 'operator-':
            self._nextToken()
            left = -self._calcAll()
        elif self.token == 'number':
            left = float(self.value)
            self._nextToken()
        elif self.token == 'var':
            if self.varList.get(self.value) == None:
                raise ValueError('Variable not found!')
            left = float(self.varList[self.value])
            self._nextToken()
        elif self.token == 'end':
            raise ValueError('Unexpected end!')
        else:
            raise ValueError('Unexpected symbol!')

        return left

    def _calcMulDiv(self):
        left = self._calcAll()

        while True:
            if self.token == 'operator*':
                self._nextToken()
                left = left * self._calcAll()

            elif self.token == 'operator/':
                lp = self.p
                self._nextToken()
                d = self._calcAll()
                if d == 0:
                    self.prev = lp
                    raise ValueError('Division by zero!')
                left = left / d
            else:
                break

        return left

    def _calcAddSub(self):
        left = self._calcMulDiv()

        while True:
            if self.token == 'operator+':
                self._nextToken()
                left = left + self._calcMulDiv()

            elif self.token == 'operator-':
                self._nextToken()
                left = left - self._calcMulDiv()

            else:
                break

        return left

    def calc(self, expr):
        self.expr = str(expr)

        self.p = 0

        self._nextToken()

        left = self._calcAddSub()

        if self.token != 'end':
            raise ValueError('Expected end!')

        return left








