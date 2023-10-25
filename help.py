import random
def SplitToShare(Num_input): 
# Alice's input
    alice_input = Num_input 

    # Generate random shares for Alice
    alice_share1 = random.randint(0, alice_input)
    alice_share2 = random.randint(0, alice_input - alice_share1)
    alice_share3 = alice_input - alice_share1 - alice_share2

    # To verify that the shares sum to Alice's input
    assert alice_share1 + alice_share2 + alice_share3 == alice_input

    print("Alice's shares:")
    print("Share 1:", alice_share1)
    print("Share 2:", alice_share2)
    print("Share 3:", alice_share3)
    result = [alice_share1,alice_share2,alice_share3] 
    return result
smth = SplitToShare(10)
