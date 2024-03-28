import argparse

parser = argparse.ArgumentParser(description="calculate the square of a number")

parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-o", "--hi", action="store_true",
                    help="say hi")
parser.add_argument("-r", "--repeat", action="count", default=0,
                    help="repeat the output")

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")
group.add_argument("-q", "--quiet", action="store_true",
                    help="make the program quiet")

args = parser.parse_args()
answer = args.square**2
for a in range(args.repeat+1):
    if args.hi:
        print('hi')
    if args.verbosity == 2:
        print("the square of {} equals {}".format(args.square, answer))
    elif args.verbosity == 1:
        print("{}^2 == {}".format(args.square, answer))
    else:
        print(answer)
return answer
