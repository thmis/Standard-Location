import math
import itertools
import pickle
import numpy
from math_utils import *

class Generator:
    '''Generates a random linear code with the highest possible transmission rate,
       builds its generation matrix in a systematic form,
       creates a dictionary for messages decoding

       Parameters:
        r — number of test characters
        n — desired maximum length of a message block transmitted
            through a communication channel
        p — probability of an error in the communication channel'''

    def __init__(self, n: int, r: int, p: float):
        t = int(p*n)
        d = 2 * t + 1
        k = n-r

        print('Start generation with t = ', t, ' d = ', d, ' k = ', k)

        if self.code_exists(n=n, k=k, d=d):
            self.t = t
            self.n = n
            self.r = r
            self.G, self.H = self.generate_matrix(n=n, k=k, d=d)
            print('Generated :')
            print('H:', self.H, sep='\n')
            print('G: ', self.G, sep='\n')
            print('Error code possibility:', self.possibility_error_of_code(n, t, p))
        else:
            raise ValueError('Can not generate code with given parameters: '
                             + 'they do not satisfy the Varshamov-Hilbert theorem')

        self.syndroms, self.codewords = self.generate_syndroms_table(n, k)

    def write_to_file(self, file_name: str):
        '''Write information adout the generated code to the file'''
        code_json = {}
        code_json['n'] = self.n
        code_json['t'] = self.t
        code_json['r'] = self.r
        code_json['Generating matrix'] = self.G
        code_json['Codewords'] = self.codewords
        code_json['Syndroms'] = self.syndroms

        with open(file_name, 'wb') as file:
            pickle.dump(code_json, file)

    def code_exists(self, n: int, k: int, d: int)->bool:
        '''Checks if given parameters satisfy the Varshamov-Hilbert theorem'''
        result = 1
        for i in range(1, d - 1):
            result += math.factorial(n - 1) / math.factorial(i) / math.factorial(n - 1 - i)

        return result < 2 ** (n - k)

    def possibility_error_of_code(self, n: int, t: int, p: float):
        '''Finds the possibility of an error in generated code'''
        result = 0
        for i in range(t + 1):
            result += (math.factorial(n) / math.factorial(i) / math.factorial(n - i)) \
                    * (p ** i) * ((1 - p) ** (n - i))

        return 1 - result


    def generate_matrix(self, n: int, k: int, d: int):
        '''Builds generating matrix in a systematic form with given k and n'''
        G_identity_matrix = numpy.eye(k, dtype=int)
        H_identity_matrix = numpy.eye(n-k, dtype=int)
        random_matrix = self.generate_random_matrix(n-k, k, d)

        result_test_matrix = [numpy.concatenate((random_matrix.T[i], H_identity_matrix[i]))
                              for i in range(len(H_identity_matrix))]

        result_generating_matrix = [numpy.concatenate((G_identity_matrix[i], random_matrix[i]))
                                    for i in range(len(G_identity_matrix))]

        return numpy.array(result_generating_matrix), numpy.array(result_test_matrix)


    def generate_random_matrix(self, r: int, k: int, d: int):
        '''Generates random matrix A where each (d-2) vectors are independent'''
        A = []
        A.append(numpy.random.randint(0, 2, r))

        for _ in range(k-1):
            linear_combinations = self.build_linear_combinations(A, r, d)

            vec = numpy.random.randint(0, 2, r)
            while is_in(vec, linear_combinations):
                vec = numpy.random.randint(0, 2, r)
            A.append(vec)

        return numpy.array(A)


    def build_linear_combinations(self, A, k: int, d: int):
        '''Builds all linear combinations as sums of 1..d-2 vectors from A'''
        combinations = []

        for vector in A:
            combinations.append(vector)

        for i in range(1, min(d-1, len(A))):
            vector_combinations = list(itertools.combinations(A, i+1))
            for vectors in vector_combinations:
                combinations.append(xor_sum(vectors, k))

        return combinations


    def generate_syndroms_table(self, n: int, k: int):
        '''Generates syndroms table for decoding'''
        syndroms_table = dict()
        codewords_table = dict()
        messages_num = 2 ** n
        codewords_num = 2 ** k

        for i in range(codewords_num):
            message = numpy.array(list(numpy.binary_repr(i, k)), dtype=int)
            coded_message = norm(numpy.matmul(message.T, self.G))
            codewords_table[''.join(map(str, coded_message))] = message

        for i in range(messages_num):
            message = numpy.array(list(numpy.binary_repr(i, n)), dtype=int)
            syndrom = binary_to_num(numpy.matmul(self.H, message.T))

            if syndrom in syndroms_table:
                syndroms_table[syndrom] = numpy.vstack((syndroms_table[syndrom], message))
            else:
                syndroms_table[syndrom] = numpy.array(message)
        return syndroms_table, codewords_table


def generate(args):
    try:
        generator = Generator(n=args.n, r=args.r, p=args.p)
        generator.write_to_file(args.out_file)
    except ValueError as error:
        print(str(error))


def encode(args):
    with open(args.in_file, 'rb') as file:
        code_json = pickle.load(file)

    n = code_json['n']
    r = code_json['r']
    t = code_json['t']
    G = code_json['Generating matrix']

    message = numpy.array(list(args.message), dtype=int)
    if len(message) != n-r:
        print('Wrong input size')
        return

    if not args.error:
        error = numpy.random.randint(0, 2, n)
        while weight(error) > t:
            error = numpy.random.randint(0, 2, n)
    else:
        error = numpy.array(list(args.error), dtype=int)
        if weight(error) > t:
            print('Invalid error vector, weight is more than', t)
            return

    if len(error) != n:
        print('Wrong error size')
        return

    encoded_message = norm(numpy.matmul(message.T, G))
    message_with_error = norm(encoded_message + error)
    print('Coded message:', ''.join(map(str, encoded_message)))
    print('Message with error:', ''.join(map(str, message_with_error)))


def decode(args):
    with open(args.in_file, 'rb') as file:
        code_json = pickle.load(file)

    n = code_json['n']
    codewords = code_json['Codewords']
    syndroms = code_json['Syndroms']
    message = numpy.array(list(args.message), dtype=int)
    if len(message) != n:
        print('Wrong input size')
        return

    print('Encoded message:', ''.join(map(str, message)))
    syndrom = find_in_dict(message, syndroms)
    if syndrom == -1:
        print('Too much errors happen!')
        return

    min_weight = 10
    error = []
    for vec in syndroms[syndrom]:
        if weight(vec) < min_weight:
            min_weight = weight(vec)
            error = vec
    print('Error:', ''.join(map(str, error)))

    message = xor_sum([error, message], n)

    print('Encoded message without error:', ''.join(map(str, message)))
    message = codewords.get(''.join(map(str, message)))
    print('Decoded message:', ''.join(map(str, message)))
