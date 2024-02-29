from classes.scanner import Scanner


# class DullRepetitiveClass:
#     def __init__(self, x ):
#         self.somemethod = self.mydecorator(self.somemethod)
#
#     def mydecorator(self, myfunction):
#         def call(*args, **kwargs):
#             print('HELLO')
#             return myfunction(*args, **kwargs)
#         return call
#
#     def somemethod(self):
#         print('SOM U')
#         return 5


if __name__ == '__main__':
    # test = DullRepetitiveClass(4)
    # test.somemethod()
    scanner = Scanner()

    scanner.start_scanner()

