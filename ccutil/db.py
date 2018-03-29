import os

DB_FILE = os.path.expanduser("~/Library/Application Support/cchelper.db")
CONFIG_FILE = os.path.expanduser("~/.ccutilparticipants")

if not os.path.exists(DB_FILE):
    f = open(DB_FILE, "w")
    f.close()

def parse_line(line):
    key, value = line.split("=")
    key = key.strip()
    value = value.strip()
    return key, value

def serialize_pair(k, v):
    return "{}={}\n".format(k.strip(), v.strip())

def set(key, value):
    new_lines = []
    if value:
        new_lines.append(serialize_pair(str(key), str(value)))

    with open(DB_FILE, "ra") as f:
        for line in f.readlines():
            if parse_line(line)[0] != str(key).strip():
                new_lines.append(line)

    with open(DB_FILE, "w") as f:
        f.writelines(new_lines)

def get(key):
    with open(DB_FILE, "r") as f:
        for line in f.readlines():
            k, v = parse_line(line)
            if k == str(key):
                return v
    return None

def group():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.readline().strip()

    return None

def participants():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f.readlines()[1:]:
                yield line.split()
