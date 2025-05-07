import unittest

from weighted_random_sampling import AliasRandomGen, CDFRandomGen, ExponentialRandomGen, LookupRandomGen

class TestRandomGen():

    generator_class = None

    def test_basic_sampling(self):
        random_nums = [1, 2, 3, 4]
        probabilities = [0.25, 0.25, 0.25, 0.25]
        gen = self.generator_class(random_nums, probabilities)
        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for _ in range(1000):
            counts[gen.next_num()] += 1
        self.assertAlmostEqual(counts[1] / 1000, 0.25, delta=0.05)
        self.assertAlmostEqual(counts[2] / 1000, 0.25, delta=0.05)
        self.assertAlmostEqual(counts[3] / 1000, 0.25, delta=0.05)
        self.assertAlmostEqual(counts[4] / 1000, 0.25, delta=0.05)

    def test_unequal_probabilities(self):
        random_nums = [1, 2, 3]
        probabilities = [0.2, 0.3, 0.5]
        gen = self.generator_class(random_nums, probabilities)
        counts = {1: 0, 2: 0, 3: 0}
        for _ in range(1000):
            counts[gen.next_num()] += 1
        self.assertAlmostEqual(counts[1] / 1000, 0.2, delta=0.15)
        self.assertAlmostEqual(counts[2] / 1000, 0.3, delta=0.15)
        self.assertAlmostEqual(counts[3] / 1000, 0.5, delta=0.15)

    def test_empty_input(self):
        random_nums = []
        probabilities = []
        with self.assertRaises(ValueError):
            self.generator_class(random_nums, probabilities)
    
    def test_probabilities_over_one(self):
        random_nums = [1, 2, 3]
        probabilities = [0.5, 0.5, 0.5]
        with self.assertRaises(ValueError):
            self.generator_class(random_nums, probabilities)
    
    def test_negative_probabilities(self):
        random_nums = [1, 2, 3]
        probabilities = [-0.1, 0.5, 0.6]
        with self.assertRaises(ValueError):
            self.generator_class(random_nums, probabilities)
    
    def test_non_numeric_probabilities(self):
        random_nums = [1, 2, 3]
        probabilities = [0.5, '0.5', 0.5]
        with self.assertRaises(TypeError):
            self.generator_class(random_nums, probabilities)
    
    def test_incorrect_length(self):
        random_nums = [1, 2, 3]
        probabilities = [0.5, 0.5]
        with self.assertRaises(ValueError):
            self.generator_class(random_nums, probabilities)

    def test_very_small_probabilities(self):
        random_nums = [1, 2, 3]
        probabilities = [0.000001, 0.999998, 0.000001]
        gen = self.generator_class(random_nums, probabilities)
        counts = {1: 0, 2: 0, 3: 0}
        for _ in range(1000):
            counts[gen.next_num()] += 1
        self.assertAlmostEqual(counts[1] / 1000, 0.000001, delta=0.05)
        self.assertAlmostEqual(counts[2] / 1000, 0.999998, delta=0.05)
        self.assertAlmostEqual(counts[3] / 1000, 0.000001, delta=0.05)

    def test_single_element(self):
        random_nums = [1]
        probabilities = [1.0]
        gen = self.generator_class(random_nums, probabilities)
        counts = {1: 0}
        for _ in range(1000):
            counts[gen.next_num()] += 1
        self.assertEqual(counts[1], 1000)
    
    def test_large_input(self):
        random_nums = list(range(10000))
        probabilities = [1/10000] * 10000
        gen = self.generator_class(random_nums, probabilities)
        counts = {i: 0 for i in range(10000)}
        for _ in range(1000):
            counts[gen.next_num()] += 1
        for i in range(10000):
            self.assertAlmostEqual(counts[i] / 1000, 1/10000, delta=0.05)


def make_test_class(generator_class):
    class_name = f"Test{generator_class.__name__}"
    return type(class_name, (TestRandomGen, unittest.TestCase), {"generator_class": generator_class})

implementations = [AliasRandomGen, CDFRandomGen, ExponentialRandomGen, LookupRandomGen]

for impl in implementations:
    globals()[f"Test{impl.__name__}"] = make_test_class(impl)

