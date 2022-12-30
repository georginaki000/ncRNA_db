import os

os.chdir(os.path.dirname(__file__))


FILENAME = "martquery_1031102737_477.txt"
DIR_NAME = "matquery_chunks"
LINES_PER_CHUNK = 50000

if os.path.isfile(FILENAME):
    print(f"Cutting {FILENAME} to chucnks")
    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)
    
    with open(FILENAME, 'r') as source:
        cur_file_num = 0
        series = "abcdefghijklmnopqrstuvwxyz"
        current_file = None
        for li, line in enumerate(source):
            if li % LINES_PER_CHUNK == 0:
                if current_file:
                    current_file.close()
                
                filepath = os.path.join(DIR_NAME, f"chunck_{series[cur_file_num]}_{FILENAME}")
                print(f"Writing to: {filepath}")
                current_file = open(filepath, 'w')
                cur_file_num += 1
            
            current_file.write(line)

        current_file.close()

else:
    print(f"Creating {FILENAME} from chunks")
    with open("gen"+FILENAME, 'w') as dest:
        chunks = sorted(os.listdir(DIR_NAME))

        for chunk_filename in chunks:
            if not chunk_filename.startswith("chunck"):
                continue

            filepath = os.path.join(DIR_NAME, chunk_filename)
            print(f"Reading from: {filepath}")
            with open(filepath, 'r') as source:
                for line in source:
                    dest.write(line)
        