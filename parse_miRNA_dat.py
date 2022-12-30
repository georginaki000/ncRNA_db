
miRNA_dat = 'miRNA.dat'


data = []

with open(miRNA_dat, 'r') as mirna_dat:
    #new = {}
    for line in mirna_dat.readlines():
        line = line.strip()

        line_split_data = line.split()
        if line.startswith('AC'):
            new = {}
            new['accessions'] = []
            new['AC'] = line_split_data[1][:-1] # skip ;
        
        elif line.startswith('SQ'):
            new['SQ'] = line.split(' '*3)[1]

        elif line.startswith("FT") and line_split_data[1].startswith("/accession="):
            accession_id = line_split_data[1].lstrip("/accession=").strip('"')
            new['accessions'].append(accession_id)
            
        # entry stop
        elif line.startswith('//'):
            data.append(new)


print(f"Read {len(data)} miRNA.dat entries")

with open('miRNAdat_accessions.csv', 'w') as out:
    out.write('AC;Accession\n')
    
    for entry in data:
        ac = entry['AC']

        for accession in entry['accessions']:
            out.write(f"{ac};{accession}\n")


# data.sort(key=lambda x : len(x['accessions']), reverse=True)
# print(*data[:10], sep='\n')

# accessinons_reversed = {}

# one_parent = True
# for mimat in data:
#     mimat_parent = mimat['AC']
#     for accession in mimat['accessions']:
#         if accession in accessinons_reversed:
#             one_parent = False
#             accessinons_reversed[accession].append(mimat_parent)
        
#         else:
#             accessinons_reversed[accession] = [mimat_parent]

# print(f"{one_parent}")
# print(accessinons_reversed)

