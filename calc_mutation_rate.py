"""
Program input is the path to a csv with the columns: 'name', 'f' and 'N'
Output is a csv with the columns: 'name', 'f', 'N' and 'u'
f = mutant frequency
N = population size
u = mutation rate per replication

This does the calculation from "A constant rate of spontaneous mutation in
DNA-based microbes" http://www.pnas.org/content/88/16/7160.full.pdf
"""
import math
import sys
import os.path


def parse_file(my_file):
    """
    Input is the path to the data file.
    Checks for a bad file path and bad headings
    skips blank lines of the file
    Returns the data as a list of lists
    :param my_file: a path
    :return:
    """
    
    if not os.path.isfile(my_file):
        sys.stdout.write("Error:  please put your data into a file named "
                         "input.csv in this folder or supply your file's "
                         "name as a command line argument.")
        sys.exit()
    
    # rU should take care of OS specific line endings
    with open(my_file, 'rU') as f:
        file_contents = f.read().split('\n')
        
    heading = file_contents[0].split(',')
    if heading[0] != "name" or heading[1] != "f" or heading[2] != "N":
        sys.stdout.write("Error:  the column headings must be name, f, N")
        sys.exit()
    
    data = [x.split(',') for x in file_contents[1:] if len(x) > 0]

    return data


def check_f_n(f, n, samp):
    """
    Input: f, n, sample name
    checks that data is valid
    Returns a warning message if invalid and "no errors" otherwise
    :param f: number
    :param n: number
    :param samp: string
    :return:
    """
    u = "no errors"
    if n <= 0:
        sys.stdout.write("Warning: N must be positive.  Please recheck "
                         "your data for sample " + samp + '\n')
        u = "n must be positive"
    if f <= 0:
        sys.stdout.write("Warning: f must be positive.  Please recheck "
                         "your data for sample " + samp + '\n')
        u = "f must be positive"
    return u


def calc_rate(n, f, u, thresh):
    """
    Estimates u given n, f, an initial guess for u, and a threshold
    Returns the estimate for u when the difference between two estimates
    is less than thresh
    :param n:
    :param f:
    :param u:
    :param thresh:
    :return:
    """

    diff = 5
    while math.fabs(diff) > thresh:

        # Safety check for log and division
        if u == 0:
            u = thresh
        if n*u == 1.0:
            u += thresh
        if n*u < 0:
            u = -u

        guess = f / math.log(n*u)
        diff = u - guess
        u = guess
        
    return u


def write_output(output, data_file):
    """
    :param output: list of string
    :param data_file: file path
    :return:
    """
    output = '\n'.join(output)

    out_file = data_file.rsplit('.')[0] + "_output_file.csv"
    with open(out_file, 'w') as f:
        f.write(output)
    print('\nThe results are in the file ' + out_file + '\n')


def main():
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = "input.csv"

    data = parse_file(data_file)
        
    output = ['name,f,N,u']
    for line in data:
        if len(line) < 3:
            sys.stdout.write("Warning:  the row \n" + ','.join(map(str, line)) +
                             "\ndoes not contain the 3 required inputs.\n")
            output.append("missing input")
        else:
            f = float(line[1])
            n = float(line[2])
            thresh = min(f, n)
            thresh /= 1000000

            u = check_f_n(f, n, line[0])
            
            if u == "no errors":
                u = str(calc_rate(n, f, f/5, thresh))
                
            output.append(','.join(line[0:3]) + ',' + u)

    write_output(output, data_file)

if __name__ == "__main__":
    main()
