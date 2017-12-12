import sys
import numpy as np
import argparse
import pygal

# pygal is installed via: pip install pygal
# If rendered graphs are black, install: lxml, tinycss and cssselect

# main execution
def main():
    parser = argparse.ArgumentParser(description='Identify if given text is k-closed')
    parser.add_argument('-k', required=False, action='store_true',
                        help='True: X=k, Y=time, lines=n. False: X=n, Y=time, lines=k.')
    parser.add_argument('-m', metavar="", type=int, required=True, nargs=1,
                        help="Minimum value of 'lines' parameter.")
    parser.add_argument('-M', metavar="", type=int, required=True, nargs=1,
                        help="Maximum value of 'lines' parameter.")
    parser.add_argument('-p', required=False, action='store_true',
                        help='True: Use pseudo-k-closed data. False: Use k-closed data')
    parser.add_argument('-r', required=False, action='store_true',
                        help='True: Data from O(nlogn) RMQs. False: Data from O(n) RMQs')
    parser.add_argument('-f', metavar="", type=str, required=True, nargs=1,
                        help='Test run filename.')

    args = parser.parse_args()
    plot_k = vars(args)['k']
    minimum = vars(args)['m'][0]
    maximum = vars(args)['M'][0]
    pseudo = vars(args)['p']
    nlogn_rmq = vars(args)['r']
    filename = vars(args)['f'][0]

    print(minimum, maximum, plot_k, pseudo, nlogn_rmq)

    with open(filename) as f:
        lines = f.read().splitlines() 

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

        if p == pseudo and r == nlogn_rmq:
            print(n, k, time)
    f.close()

    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart.render_to_file('./chart.svg')
    
# call main
if __name__ == "__main__":
    main()
