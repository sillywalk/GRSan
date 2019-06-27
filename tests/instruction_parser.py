import os
import argparse
import re
import sys

def get_more_info(filename):
    with open(filename) as f:
        content = f.readlines()
    def helper(pattern, name, verbose=False):
        location = None
        storage = None
        found = False
        for idx, line in enumerate(content):
            if re.search(pattern, line):
                found = True
                storage = line.strip()
                location = " @ %s:%d" % (filename, idx+1)
                break
        if not found:
            print("Error could not find %s %s" % (name, pattern))
        if verbose:
            print("found %s--> %s" % (name, storage+location))
        return storage
    return helper

def build_line(f, insn_id):
    pattern = "!\d+ = !{i64 %d}" % (insn_id)
    storage = more_info_ftn(pattern, "gradmetadata")
    if storage is None:
        return "unknown for instruction_id %s" % (str(insn_id))
    pattern = "!GRAD !%s" % (storage.split()[0][1:].strip())
    storage = more_info_ftn(pattern, "instruction")
    instruction = storage
    if "dbg" in storage:
        pattern = "!%s = " % (storage.split('!dbg ')[1].split(',')[0][1:].strip())
        storage = more_info_ftn(pattern, "dbginfo")
        linenumber = storage.split('line: ')[1].split(',')[0].strip().replace(")", "")
        try:
            column_number = storage.split('column: ')[1].split(',')[0].strip().replace(")", "")
        except:
            print("Error finding column number for %s" % (storage))
            column_number = "unknown"
        pattern = "!%s = " % (storage.split('scope: ')[1].split(',')[0][1:].strip().replace(")", ""))
        storage = more_info_ftn(pattern, "subprogram")
        pattern = "!%s = " % (storage.split('file: ')[1].split(',')[0][1:].strip())
        storage = more_info_ftn(pattern, "file")
        filename = storage.split('filename: ')[1].split(',')[0].strip().replace(")", "").replace('"', "")
        return "%s --> %s:%s, col %s" % (instruction, filename, linenumber, column_number)
    else:
        return "%s --> no debug info" % (instruction)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to associate a dfsan insn id with instruction in the .ll file')
    parser.add_argument('filename', type=str,
                                help='Path to .ll file')
    parser.add_argument('metadata', type=str,
            help='either the path to a *.txt file representing the derivative dump or the insn id, typically the XXX in insnID: XXX in hello.txt')
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        parser.error("%s does not exist" % args.filename)
    more_info_ftn = get_more_info(args.filename)
    # handle a particular instruction id
    if args.metadata.isdigit():
        print(build_line(more_info_ftn, int(args.metadata)))
    else:
        # annotate a file
        if not os.path.exists(args.metadata):
            parser.error("%s does not exist" % args.filename)
        if os.path.splitext(args.metadata)[1] == '.txt':
            with open(args.metadata) as f:
                content = f.readlines()
            annotations = []
            size = len(content)
            for idx, line in enumerate(content):
                print("%d/%d" % (idx, size))
                insnIDSplit = line.split("insnID: ")
                if len(insnIDSplit) > 1:
                    annotations.append(line.replace("\n", "") + "--" + build_line(more_info_ftn, int(insnIDSplit[1].split(" ")[0])))
            with open("annotated-%s" % (args.metadata), "w") as f:
                f.write("\n".join(annotations))
