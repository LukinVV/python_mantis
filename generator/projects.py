from model.project import Project
import random
import string
import os.path
import jsonpickle
import getopt
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contacts", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 3
f = "data/projects.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters * 5 + string.digits * 3
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


statuses = ["development", "release", "stable", "obsolete"]

checkbox_values = ["yes", "no"]

view_statuses = ["public", "private"]


testdata = [
    Project(name=random_string("name", 10), status=random.choice(statuses), enabled = random.choice(checkbox_values),
            inherit_gl_categories=random.choice(checkbox_values), view_status=random.choice(view_statuses),
            description=random_string("description", 30))
    for i in range(n)
]




file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))