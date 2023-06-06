def wrap(input_func):
    def output_func(*args):
        a = args[0]
        b = args[1]
        print(type(args))
        print(args)
        return input_func(a, b)
    return output_func

@wrap
def razn(a, b):
    return b - a

razn(4, 5)

new_list = [i+1 for i in range(10)]

lst = list(map(lambda x: x%2 == 0, new_list))


