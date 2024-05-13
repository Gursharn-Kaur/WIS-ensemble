'''
    read a text file containing all quantiles.
    
    takes a argument-- fname.
    
    fname: str, default='alpha.txt'. file name (location) of the quantiles.
    
    Returns-
    
    alphas: containing all quantiles.
'''


def get_alpha(fname='alpha.txt'):
    f_alpha = open(fname,'r')
    read_alpha = f_alpha.readlines()[0].split(' ')
    alphas = [float(a) for a in read_alpha]
    return alphas


