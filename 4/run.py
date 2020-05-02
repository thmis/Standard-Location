from argparse import ArgumentParser
import coder


def run():
    '''Parse argument of the command line'''
    parser = ArgumentParser(prog='coder', description='Linear error-correcting codes')
    subparsers = parser.add_subparsers(title='mode', description='Working mode')

    generation_mode = subparsers.add_parser('generate',
                                            help='Generates linear code with given parameters')
    generation_mode.add_argument('-r', dest='r', type=int, help='number of test characters', 
                                 required=True)
    generation_mode.add_argument('-n', dest='n', type=int, help='desired maximum length of a '
                                 + 'message block transmitted through a communication channel',
                                 required=True)
    generation_mode.add_argument('-p', dest='p', type=float, help='probability of an error in the '
                                 + 'communication channel', required=True)
    generation_mode.add_argument('-o', dest='out_file', type=str, default='code.data',
                                 help='file with information for coder and decoder', required=True)
    generation_mode.set_defaults(func=coder.generate)

    encode_mode = subparsers.add_parser('encode', help='Encodes message with an error')
    encode_mode.add_argument('-i', dest='in_file', type=str, help='file with information for coder',
                             required=True)
    encode_mode.add_argument('-m', dest='message', type=str, help='message to encode',
                             required=True)
    encode_mode.add_argument('-e', dest='error', type=str, help='error to add to encoded message', default=None)
    encode_mode.set_defaults(func=coder.encode)

    decode_mode = subparsers.add_parser('decode', help='Finds error and decodes message')
    decode_mode.add_argument('-i', dest='in_file', type=str, help='file with information for decoder',
                             required=True)
    decode_mode.add_argument('-m', dest='message', type=str, help='message to decode', required=True)
    decode_mode.set_defaults(func=coder.decode)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    run()
