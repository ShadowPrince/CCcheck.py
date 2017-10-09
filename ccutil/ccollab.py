import subprocess
import os
import re
import pipes

from utils import verbose

TEE_FILE = "/tmp/cc_output"

def review_url(id):
    return "https://laxm1bapps565.ent.core.medtronic.com/ui#review:id={}".format(id)

def call_ccollab(*args):
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

    print("sh > {}".format(line))
    if raw_input("run it? y/n > ") != "y":
        return

    os.system(line)
    #with open("/Users/vasyl.horbachenko/projects/_Misc/CCcheck/samples/ccollab_addchanges_new", "r") as f:
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

def update_review(id, title, group, overview):
    args = ["admin", "review", "edit", id,
            "--title", title,
            "--custom-field", "Feature=Unknown",
            "--custom-field", "Overview={}".format(overview), ]
    if group:
        args += ["--group", group, ]

    call_ccollab(*args)
