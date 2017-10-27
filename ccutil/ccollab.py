import subprocess
import os
import re
import pipes
from xml.etree import ElementTree

from utils import verbose

TEE_FILE = "/tmp/cc_output"

def review_url(id):
    return "https://laxm1bapps565.ent.core.medtronic.com/ui#review:id={}".format(id)

def call_ccollab(*args):
    args = ["ccollab", "--no-browser", "--non-interactive"] + list(args)
    verbose("sh > {}".format(" ".join(args)))
    output = subprocess.check_output(args)
    verbose(output)

    return output

def create_new_review(files):
    lines = call_ccollab("addchanges", "new", *files).splitlines()

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

def review_files_changed(reviewid):
    output = call_ccollab("admin", "review-xml", str(reviewid))

    xml = ElementTree.fromstring(output)

    result = {}
    for artifact in xml.iter("artifact"):
        result[artifact.find("path").text] = artifact.find("scmVersion").text

    return result

