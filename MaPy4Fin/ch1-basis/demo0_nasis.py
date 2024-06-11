"""
面向对象
"""
class Hello(object):
    def __init__(self, mySay) -> None:
        self.mySay = mySay

    def sayHello(self, name):
        print ('{} {}'.format(self.mySay, name))

"""
函数式编程
"""
from functools import partial
def greetings(my_greeting, name):
    print('{} {}'.format(my_greeting, name))

def main_greet():
    say_hello_to = partial(greetings, "Hello")
    say_hello_to('World')

if __name__ == '__main__':
    hello = Hello("Hello")
    hello.sayHello('Cat')
    main_greet()