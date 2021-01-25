import os
import sys
import re
import subprocess
import time
from subprocess import CalledProcessError, TimeoutExpired

STATUS_CODES = {
    200: 'Ok',
    201: 'Accepted',
    400: 'Wrong Answer',
    401: 'Compilation Error',
    402: 'Runtime Error',
    403: 'Invalid File',
    404: 'File Not Found',
    408: 'Time Limit Exceeded'
}


class Judge:
    # Class that judges given code with given input and output files and time limit

    def __init__(self, filename, input_file, expected_output_file, time_limit):
        """Receives a name of a file from the userIt must be a valid c, c++, java file """
        self.fileName = filename  # Full name of the source code file
        self.language = None  # Language
        self.name = None  # File name without extension
        self.inputFile = input_file  # Input file
        self.expectedOutputFile = expected_output_file  # Expected output file
        self.actualOutputFile = 'output.txt'  # Actual output file
        self.timeLimit = time_limit  # Time limit set for execution in seconds
        self.memory_limit = '1024'

    def is_valid_file(self):
        """ Checks if the filename is valid """
        valid_file = re.compile("^(\S+)\.(java|cpp|c|py)$")
        matches = valid_file.match(self.fileName)
        if matches:
            self.name, self.language = matches.groups()
            return True
        return False

    @staticmethod
    def x(f):
        return f.split('/')[-1]

    @staticmethod
    def compare(file1, file2):
        f1 = open(file1, 'r')
        f2 = open(file2, 'r')
        l1 = f1.read().rstrip()
        l2 = f2.read().rstrip()
        return l1 == l2

    def compile(self):
        """ Compiles the given program, returns status code and errors """
        # Remove previous executables
        if os.path.isfile(self.name):
            os.remove(self.name)

        # Check if media are present
        if not os.path.isfile(self.fileName):
            return 404, 'Missing file'

        # Check language
        cmd = None
        if self.language == 'java':
            cmd = ['javac', self.fileName]
        elif self.language == 'c':
            cmd = ['gcc', '-o', self.name, self.fileName]
        elif self.language == 'cpp':
            cmd = ['g++', '-o', self.name, self.fileName]
        elif self.language == 'py':
            return 200, None

        # Invalid media
        if cmd is None:
            return 403, 'File is of invalid type'

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # Check for errors
            if proc.returncode != 0:
                error_line = proc.stderr.split('\n')[0].split(':')[1]
                error_code = proc.stderr.split('\n')[1]
                return 401, 'Compilation error on line {}: {}'.format(error_line, error_code)
            else:
                return 200, None
        except CalledProcessError as e:
            print(e.output)

    def run(self):
        """ Runs the executable, returns status code and errors """
        # Check if media are present
        if not os.path.isfile(self.fileName):
            return 404, 'Missing executable file'

        # Check language
        cmd = None
        if self.language == 'java':
            cmd = ['java', self.name]
        elif self.language in ['c', 'cpp']:
            cmd = self.name
        elif self.language == 'py':
            cmd = ['python', self.fileName]

        # Invalid media
        if cmd is None:
            return 403, 'File is of invalid type'

        try:
            with open('output.txt', 'w+') as fout:
                fin = None
                if self.inputFile and os.path.isfile(self.inputFile):
                    fin = open(self.inputFile, 'r')
                st = time.time()
                proc = subprocess.run(
                    cmd,
                    stdin=fin,
                    stdout=fout,
                    stderr=subprocess.PIPE,
                    timeout=self.timeLimit,
                    universal_newlines=True,
                )
                tt = int((time.time() - st) * 100)
            # Check for errors
            if proc.returncode != 0:
                return 402, proc.stderr
            else:
                return 200, None
        except TimeoutExpired as tle:
            return 408, tle
        except CalledProcessError as e:
            print(e.output)

        # Perform cleanup
        if self.language == 'java':
            os.remove('{}.class'.format(self.name))
        elif self.language in ['c', 'cpp']:
            os.remove(self.name)

    def match(self):
        if os.path.isfile(self.actualOutputFile) and os.path.isfile(self.expectedOutputFile):
            result = self.compare(self.actualOutputFile, self.expectedOutputFile)
            if result:
                return 201, None
            else:
                return 400, None
        else:
            return 404, 'Missing output media'

    def code_checker(self, check=True):
        if self.is_valid_file():
            print('Executing code checker...')
            # Compile program
            compile_result, compile_errors = self.compile()
            print('Compiling... {0}({1})'.format(STATUS_CODES[compile_result], compile_result), flush=True)
            if compile_errors is not None:
                sys.stdout.flush()
                print(compile_errors, file=sys.stderr)
                return compile_result
            # Run program
            runtime_result, runtime_errors = self.run()
            print('Running... {0}({1})'.format(STATUS_CODES[runtime_result], runtime_result), flush=True)
            if runtime_errors is not None:
                sys.stdout.flush()
                print(runtime_errors, file=sys.stderr)
                return runtime_result

            if check:
                # Match expected output
                match_result, match_errors = self.match()
                print('Verdict... {0}({1})'.format(STATUS_CODES[match_result], match_result), flush=True)
                if match_errors is not None:
                    sys.stdout.flush()
                    print(match_errors, file=sys.stderr)
                    return match_errors
                return match_result
        else:
            print('FATAL: Invalid file', file=sys.stderr)
            return 403


# j = Judge(filename='temp/add.cpp', input_file='temp/input.txt', expected_output_file='temp/ex_output.txt',
#           time_limit=2)
# print(STATUS_CODES[j.code_checker()])