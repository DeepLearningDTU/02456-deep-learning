__author__ = 'casperkaae'
import numpy as np

target_to_text = {
    '0':'zero',
    '1':'one',
    '2':'two',
    '3':'three',
    '4':'four',
    '5':'five',
    '6':'six',
    '7':'seven',
    '8':'eight',
    '9':'nine',
}

stop_character = '#'

input_characters = " ".join(target_to_text.values())
valid_characters = ['0', '1', '2', '3',  '4',  '5',  '6',  '7',  '8',  '9',  '#'] + \
              list(set(input_characters))

def print_valid_characters():
    l = ''
    for i,c in enumerate(valid_characters):
        l += "\'%s\'=%i,\t" % (c,i)
    print "Number of valid characters:", len(valid_characters)
    print l

ninput_chars = len(valid_characters)
def get_batch(batch_size=100, min_digits = 3, max_digits=3):
    '''
    Generates random sequences of integers and translates them to text i.e. 1->'one'.
    :param batch_size: number of samples to return
    :param min_digits: minimum length of target
    :param max_digits: maximum length of target
    '''
    text_inputs = []
    int_inputs = []
    text_targets = []
    int_targets = []
    for i in range(batch_size):
        #convert integer into a list of digits
        tar_len = np.random.randint(min_digits,max_digits+1)
        text_target = "".join(map(str,np.random.randint(0,10,tar_len))) + stop_character
        inp_str = text_target[:-1]

        #generate the targets as a list of intergers
        int_target = map(lambda c: valid_characters.index(c), text_target)

        #generate the text input
        text_input = " ".join(map(lambda k: target_to_text[k], inp_str))
        #generate the inputs as a list of intergers
        int_input = map(lambda c: valid_characters.index(c), text_input)

        text_inputs.append(text_input)
        int_inputs.append(int_input)
        text_targets.append(text_target)
        int_targets.append(int_target)

    #create the input matrix and mask - note that we zero pad the shorter sequences.
    max_input_len = max(map(len,int_inputs))
    inputs = np.zeros((batch_size,max_input_len))
    input_masks = np.zeros((batch_size,max_input_len))
    for (i,inp) in enumerate(int_inputs):
        cur_len = len(inp)
        inputs[i,:cur_len] = inp
        input_masks[i,:cur_len] = 1

    targets = np.zeros((batch_size,max_digits+1)) #+1 to allow space for stop character
    target_masks = np.zeros((batch_size,max_digits+1)) #+1 to allow space for stop character
    for (i,tar) in enumerate(int_targets):
        cur_len = len(tar)
        targets[i,:cur_len] = tar
        target_masks[i,:cur_len] = 1

    return inputs.astype('int32'), \
           input_masks.astype('float32'), \
           targets.astype('int32'), \
           target_masks.astype('float32'), \
           text_inputs, \
           text_targets

