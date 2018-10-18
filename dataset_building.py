import os
from random import shuffle
import np as np

input_dotbrackets = []
input_sequences = []
input_ids = []
len_limit = 700 # 2000 è l'ideale

input_list = os.listdir('data')
shuffle(input_list)

np.random.seed(7)

for filename in input_list:
  sequence = []
  dotbracket = []
  num_lines = sum(1 for line in open('data/'+filename)
             if not line.startswith('# ') 
             and len(line)>0 
             and line != '\n')
  
  raw_file = open('data/'+filename).read().splitlines()
  
  for line in raw_file:
    if (not line.startswith('# ') and len(line)>0 and line != '\n'):
      if(len(sequence)>= (num_lines/2)):
        dotbracket.append(line)
      else:
        sequence.append(line)
  
  s = ''.join(sequence)
  d = ''.join(dotbracket)
  
  if(len(s)<len_limit):
    input_sequences.append(s)
    input_dotbrackets.append(d)
    input_ids.append(filename)
    
print("number of raw sequences in input: {}".format(len(input_sequences))) # total: 3554 sequences

token_index_seq = {}
token_index_db = {}

for sequence in input_sequences:
  for base in sequence:
    if base not in token_index_seq:
      token_index_seq[base] = len(token_index_seq)+1
      
for db_sequence in input_dotbrackets:
  for base in db_sequence:
    if base not in token_index_db:
      token_index_db[base] = len(token_index_db)+1

print("characters in the sequences dictionary (full): {}".format(len(token_index_seq)))
print("characters in the dotbrackets dictionary (full): {}".format(len(token_index_db)))
print()
sorted_by_value = sorted(token_index_seq.items(), key=lambda kv: kv[1])
print("dictionary for sequences")
print(sorted_by_value)
print()
sorted_by_value = sorted(token_index_db.items(), key=lambda kv: kv[1])
print("dictionary for dotbrackets")
print(sorted_by_value)

max_length = len(max(input_sequences, key=len))
print('Filtering now the dictionary in order to remove the seqs with the chars not allowed; allowed values are:')
allowed_dictionary_seq = ['A', 'C', 'G', 'U', 'M', 'N', 'R', 'W', 'S', 'Y', 'K', 'V', 'H', 'D', 'B']
print(allowed_dictionary_seq)
print()
input_sequences_temp = []
input_dotbrackets_temp = []
input_ids_temp = []
token_index_seq_temp = dict(token_index_seq)
#token_index_seq
print("token_index_seq:")
sorted_by_value = sorted(token_index_seq.items(), key=lambda kv: kv[1])
print(sorted_by_value)
#for val in allowed_dictionary_seq:
#  handleNull = token_index_seq.pop(val, None)
token_index_seq_final = {key: value+1 for (value, key) in enumerate(allowed_dictionary_seq)}
#token_index_seq['EOS'] = len(token_index_seq)
for char in token_index_seq_final.keys():
  if char not in allowed_dictionary_seq:
    handleNull = token_index_seq_final.pop(val, None)
print()
print("final dict for sequences:")
sorted_by_value = sorted(token_index_seq_final.items(), key=lambda kv: kv[1])

for sequence,db,fname in zip(input_sequences, input_dotbrackets, input_ids):
  copy_it = True
  for char in sequence:
    if char not in token_index_seq_final.keys():
      copy_it = False
  if copy_it == True:
    input_sequences_temp.append(sequence)
    input_dotbrackets_temp.append(db)
    input_ids_temp.append(fname)

input_sequences = input_sequences_temp
input_dotbrackets = input_dotbrackets_temp
input_ids = input_ids_temp

input_x = np.zeros((len(input_sequences), max_length, max(token_index_seq_final.values())+1))

for i, sequence in enumerate(input_sequences):
  for j, base in enumerate(sequence):
    index = token_index_seq_final.get(base)
    input_x[i, j, index] = 1
    if j == len(sequence)-1:
      if j != max_length-1:
        input_x[i, j+1:max_length, 0] = 1
        
input_y = np.zeros((len(input_dotbrackets), max_length, max(token_index_db.values()) + 1))

for i, sequence in enumerate(input_dotbrackets):
  for j, base in enumerate(sequence):
    index = token_index_db.get(base)
    input_y[i, j, index] = 1
    if j == len(sequence)-1:
      if j != max_length-1:
        input_y[i, j+1:max_length, 0] = 1
        
input_shape = input_x[0].shape
output_shape = input_y[0,0,:].shape[0]
