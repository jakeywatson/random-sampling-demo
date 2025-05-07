from weighted_random_sampling import AliasRandomGen, CDFRandomGen, ExponentialRandomGen, LookupRandomGen

def main():
    """
    Main function to demonstrate the usage of different random number generators.
    It creates instances of each generator and generates random numbers based on the initialized probabilities.
    The generated random numbers are printed to the console.
    The random number generators used are:
    1. AliasRandomGen
    2. CDFRandomGen
    3. ExponentialRandomGen
    4. LookupRandomGen
    """
    random_nums = [1, 2, 3, 4]
    probabilities = [0.25, 0.25, 0.25, 0.25]

    alias_gen = AliasRandomGen(random_nums, probabilities)
    cdf_gen = CDFRandomGen(random_nums, probabilities)
    exp_gen = ExponentialRandomGen(random_nums, probabilities)
    lookup_gen = LookupRandomGen(random_nums, probabilities)

    print("AliasRandomGen:")
    for _ in range(10):
        print(alias_gen.next_num())

    print("\nCDFRandomGen:")
    for _ in range(10):
        print(cdf_gen.next_num())

    print("\nExponentialRandomGen:")
    for _ in range(10):
        print(exp_gen.next_num())

    print("\nLookupRandomGen:")
    for _ in range(10):
        print(lookup_gen.next_num())


if __name__ == "__main__":
    main()