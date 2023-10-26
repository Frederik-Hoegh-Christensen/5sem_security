import random
def split_num_to_shares(input): 

    input = input 
    
    share1 = random.randint(0, input)
    share2 = random.randint(0, input - share1)
    share3 = input - share1 - share2

    assert share1 + share2 + share3 == input

    
    result = [share1,share2,share3] 
    return result

