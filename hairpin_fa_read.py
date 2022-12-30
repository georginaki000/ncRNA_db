import os

os.chdir(os.path.dirname(__file__))

# fa files
def fa_file_seq_join(filename):
    correct = []
    mistakes = []
    with open(filename, 'r') as f:
        build_seq = ""
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if build_seq != "" and ("Homo" in line or "sapiens" in line):
                    correct.append(build_seq)
                else:
                    mistakes.append(build_seq)
                build_seq = ""
                
            else:
                build_seq += line
                mistakes.append(line)
    
    return set(correct), set(mistakes)

corr, mis = fa_file_seq_join("hairpin.fa")

with open("hairpin_fa_correct_human.txt", 'w') as cf:
    for c in corr:
        cf.write(c+"\n")

with open("hairpin_fa_mistakes.txt", 'w') as mf:
    for m in mis:
        mf.write(m+"\n")