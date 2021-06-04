"""
Dict Union 은 Python 3.9 에 추가된 기능(그 이전 버전은 구동 안 됨)
- https://www.python.org/dev/peps/pep-0584/#id18
- https://www.python.org/dev/peps/pep-0584/#specification

병합 연산자 '|' 를 이용하여 Dictionary 를 병합할 수 있다. 
- 참고 문서 : https://betterprogramming.pub/new-union-operators-to-merge-dictionaries-in-python-3-9-8c7dbbd1080c
"""

# 1
d = {'spam': 1, 'eggs': 2, 'cheese': 3}
e = {'cheese': 'cheddar', 'aardvark': 'Ethel'}

print(d | e)
"""
Dict union will return a new dict consisting of the left operand merged with the right operand, 
each of which must be a dict (or an instance of a dict subclass). If a key appears in both operands, 
the last-seen value (i.e. that from the right-hand operand) wins:

{'spam': 1, 'eggs': 2, 'cheese': 'cheddar', 'aardvark': 'Ethel'}
"""

# 2
print(e | d)

"""
{'cheese': 3, 'aardvark': 'Ethel', 'spam': 1, 'eggs': 2}
"""

# 3
d |= e
print(d)

"""
{'spam': 1, 'eggs': 2, 'cheese': 'cheddar', 'aardvark': 'Ethel'}
"""

# 4
d |= [('spam', 999)]
print(d)

"""
{'spam': 999, 'eggs': 2, 'cheese': 'cheddar', 'aardvark': 'Ethel'}
"""