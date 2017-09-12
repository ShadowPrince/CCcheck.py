import subprocess
import os
import re
import pipes

from utils import verbose

TEE_FILE = "/tmp/cc_output"

def review_url(id):
    return "https://laxm1bapps565.ent.core.medtronic.com/ui#review:id={}".format(id)

def call_ccollab(*args):
    global TEE_FILE
    cmd = "ccollab"
    default_args = ["--no-browser", "--non-interactive",  ]
    args = [pipes.quote(x) for x in default_args + list(args)]

    line = "{} {} | tee {}".format(
            cmd,
            " ".join(args),
            TEE_FILE
            )

    try:
        os.remove(TEE_FILE)
    except OSError:
        pass

    verbose("sh > {}".format(line))
    os.system(line)
    #TEE_FILE = "/Users/vasyl.horbachenko/projects/_Misc/CCcheck/samples/ccollab_addchanges_new"
    with open(TEE_FILE, "r") as f:
        lines = f.readlines()
        if not len(lines):
            raise Exception("ccollab didn't output anything!")

        return lines

def create_new_review(files):
    lines = call_ccollab("addchanges", "new", *files)

    try:
        review_id = int(re.findall(r"\w+ (\d+).", lines[-1])[0])
    except Exception:
        raise Exception("Failed to get review id!")

    return review_id

def append_to_review(id, files):
    call_ccollab("addchanges", id, *files)
