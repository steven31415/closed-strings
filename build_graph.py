import sys
import numpy as np
import argparse
import pygal
import math

# pygal is installed via: pip install pygal
# If rendered graphs are black, install: lxml, tinycss and cssselect

# main execution
def main():
    parser = argparse.ArgumentParser(description='Identify if given text is k-closed')
    parser.add_argument('-k', required=False, action='store_true',
                        help='True: X=k, Y=time, lines=n. False: X=n, Y=time, lines=k.')
    parser.add_argument('-mL', metavar="", type=int, required=True, nargs=1,
                        help="Minimum value of 'lines' parameter.")
    parser.add_argument('-ML', metavar="", type=int, required=True, nargs=1,
                        help="Maximum value of 'lines' parameter.")
    parser.add_argument('-mX', metavar="", type=int, required=True, nargs=1,
                        help="Minimum value of 'X' parameter.")
    parser.add_argument('-MX', metavar="", type=int, required=True, nargs=1,
                        help="Maximum value of 'X' parameter.")
    parser.add_argument('-p', required=False, action='store_true',
                        help='True: Use pseudo-k-closed data. False: Use k-closed data')
    parser.add_argument('-r', required=False, action='store_true',
                        help='True: Data from O(nlogn) RMQs. False: Data from O(n) RMQs')
    parser.add_argument('-f', metavar="", type=str, required=True, nargs=1,
                        help='Test run filename.')

    args = parser.parse_args()
    plot_k = vars(args)['k']
    minimum_L = vars(args)['mL'][0]
    maximum_L = vars(args)['ML'][0]
    minimum_X = vars(args)['mX'][0]
    maximum_X = vars(args)['MX'][0]
    pseudo = vars(args)['p']
    nlogn_rmq = vars(args)['r']
    filename = vars(args)['f'][0]

    with open(filename) as f:
        lines = f.read().splitlines() 

    n_values = []
    k_values = []
    p_values = []
    r_values = []
    time_values = []

    for line in lines:
        if line in ['\n', '\r\n']:
            continue
        if line[0] in ['#', 'n']:
            continue

        data = line.split(" ")
        n = int(data[0])
        k = int(data[1])
        p = bool(int(data[2]))
        r = bool(int(data[3]))

        time = float(data[4])

        n_values.append(n)
        k_values.append(k)
        p_values.append(p)
        r_values.append(r)
        time_values.append(time)

    f.close()

    n_unique_values = []
    for x in n_values:
        if x not in n_unique_values:
        	n_unique_values.append(x)

    k_unique_values = []
    for x in k_values:
        if x not in k_unique_values:
            k_unique_values.append(x)

    if plot_k == False:
        line_chart = pygal.XY(x_label_rotation=-90, show_only_major_dots=True, x_title='n', y_title='seconds')
        line_chart.title = 'Algorithm run time'
        
        x_labels = []

        for n in n_unique_values:
            if n >= minimum_X and n <= maximum_X:
                x_labels.append({
                'label': str(n),
                'value': n
                })

        line_chart.x_labels = x_labels

        for k in k_unique_values:
            if k >= minimum_L and k <= maximum_L:
                points = []
                for i in range(0, len(time_values)):
                    if p_values[i] == pseudo and r_values[i] == nlogn_rmq and k_values[i] == k:
                       if n_values[i] >= minimum_X and n_values[i] <= maximum_X:
                            points.append((n_values[i], time_values[i]))

                line_chart.add('K=' + str(k), points)

        line_chart.render_to_file('./chart.svg')
        
# call main
if __name__ == "__main__":
    main()
