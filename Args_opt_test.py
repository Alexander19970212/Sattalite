from scipy.optimize import differential_evolution

def func(parameters, *data):

    #we have 3 parameters which will be passed as parameters and
    #"experimental" x,y which will be passed as data

    a,b,c = parameters
    x,y = data

    result = 0

    for i in range(len(x)):
        result += (a*x[i]**2 + b*x[i]+ c - y[i])**2

    return result**0.5

if __name__ == '__main__':
    #initial guess for variation of parameters
    #             a            b            c
    bounds = [(-1, 0.5), (-0.3, 0.3), (0.1, -0.1)]

    #producing "experimental" data
    x = [i for i in range(6)]
    y = [x**2 for x in x]

    #packing "experimental" data into args
    args = [x,y]
    print(args)

    result = differential_evolution(func, bounds, args=args)
    print(result.x)