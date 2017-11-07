from MathParser import MathParser

m = MathParser()

print('a = 1000')
m.setValue('a', 1000)

print('1 + 3 * a + 10')
print(m.calc('1 + 3 * a + 10'))