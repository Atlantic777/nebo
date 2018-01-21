import json


class Job:
    def __init__(self, input_file, output_file,
                 raw_msg=None):
        self.input_file = input_file
        self.output_file = output_file
        self.raw_msg = raw_msg

        print(input_file)
        print(output_file)

    def work(self):
        request = json.loads(self.raw_msg)
        keywords = request['args']

        keywords = keywords.replace(' ', '')
        keywords = keywords.split(',')

        retval = {}

        for word in keywords:
            retval[word] = 0

        with open(self.input_file) as inp:
            for line in inp.readlines():
                for word in keywords:
                    if word in line:
                        retval[word] += 1

        with open(self.output_file, "w") as out:
            out.write(json.dumps(retval))
