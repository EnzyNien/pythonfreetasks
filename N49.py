import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
sp.init_printing(use_latex='mathjax')


class Diff():

    @staticmethod
    def clean_data(data):
        data = data.replace('^', '**')
        data = data.replace(' ', '')
        #try
        return parse_expr(data)
        #except

    @staticmethod
    def make_diff():
        x = sp.Symbol('x')
        print('Enter the polynomial to determine the derivative...')
        print('example "x^2 + sin(x)/cos(x-1)"')
        while True:
            data = input("==> ").lower()
            data = Diff.clean_data(data)
            data.free_symbols
            res = data.diff(*list(data.free_symbols))
            res = sp.simplify(res)
            print("<== {0}".format(res))

if __name__ == '__main__':
    Diff.make_diff()
