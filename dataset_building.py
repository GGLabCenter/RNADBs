import os
from random import shuffle
import numpy as np
from sklearn.model_selection import train_test_split

input_dotbrackets = []
input_sequences = []
input_ids = []
len_limit = 700

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
    input_sequences.append(s+'\n')
    input_dotbrackets.append(d+'\n')
    input_ids.append(filename)

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

max_length = len(max(input_sequences, key=len))
allowed_dictionary_seq = ['\n', 'A', 'C', 'G', 'U', 'M', 'N', 'R', 'W', 'S', 'Y', 'K', 'V', 'H', 'D', 'B']

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


base_to_idx = set()
db_to_idx = set()
for sequence in input_sequences:
  for base in sequence:
    if (base not in base_to_idx):
      base_to_idx.add(base)
for sequence in input_dotbrackets:
  for dbr in sequence:
    if (dbr not in db_to_idx):
      db_to_idx.add(dbr)
base_to_idx = sorted(list(base_to_idx))
db_to_idx = sorted(list(db_to_idx))
base_to_idx_dict = {}
idx_to_base_dict = {}
for k, v in enumerate(base_to_idx):
    idx_to_base_dict[k] = v
    base_to_idx_dict[v] = k
db_to_idx_dict = {}
idx_to_db_dict = {}
for k, v in enumerate(db_to_idx):
    idx_to_db_dict[k] = v
    db_to_idx_dict[v] = k  
max_len_sequence = max([len(line) for line in input_sequences])
max_len_db = max([len(line) for line in input_dotbrackets])
base_to_idx_dict
print()
print()
idx_to_db_dict
print()
max_len_sequence
print()
max_len_db

input_x = np.zeros((len(input_sequences), max_len_sequence, len(base_to_idx)))

for i, sequence in enumerate(input_sequences):
  for j, base in enumerate(sequence):
    index = base_to_idx_dict.get(base)
    input_x[i, j, index] = 1
    # added the Masking Layer:
    #if j == len(sequence)-1:
    #if j != max_len_sequence-1:
    #input_x[i, j+1:max_len_sequence, 0] = 1
        
input_y = np.zeros((len(input_dotbrackets), max_len_db, len(db_to_idx)))

for i, sequence in enumerate(input_dotbrackets):
  for j, base in enumerate(sequence):
    index = db_to_idx_dict.get(base)
    input_y[i, j, index] = 1
    # added the Masking Layer:
    # if j == len(sequence)-1:
    # if j != max_len_db-1:
    # input_y[i, j+1:max_len_db, 0] = 1
        

x_train, x_test, y_train, y_test = train_test_split(input_x, input_y, shuffle=True, test_size=50)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, shuffle=True, test_size=0.20)

input_shape = x_train[0].shape
output_shape = y_train[0,0,:].shape[0]
