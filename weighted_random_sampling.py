import random
import math

import numpy as np  

from decimal import Decimal

"""
Weighted Random Sampling
This module provides different classes for generating random numbers based on given probabilities.
The classes include:
1. AliasRandomGen: Uses the alias method for efficient sampling.
2. CDFRandomGen: Uses cumulative distribution function for sampling.
3. ExponentialRandomGen: Uses exponential distribution for sampling.
4. LookupRandomGen: Uses a lookup table for sampling.
Each class has a method `next_num()` that returns a random number based on the initialized probabilities.
"""
class RandomGen(object):  
    # Values that may be returned by next_num()  
    _random_nums = []  
    # Probability of the occurence of random_nums  
    _probabilities = []  
    
    def next_num(self):  
        """  
        Returns one of the randomNums. When this method is called multiple 
        times over a long period, it should return the numbers roughly with 
        the initialized probabilities.  
        """
        pass

    def verify_input_correctness(self):
        """  
        Checks that the inputs provided to the class are correct. If not, raise Error.
        The following checks are performed:
        1. Length of arrays are the same.
        2. No illegal values present.
        3. Sum of probabilities is 1.
        """

        if len(self._probabilities) != len(self._random_nums):
            raise ValueError("Length of probabilities and random numbers set must be the same.")
        
        if any(not isinstance(num, (int, float)) for num in self._random_nums):
            raise ValueError("Random numbers must be integers or floats.")
        
        if any(prob < 0 for prob in self._probabilities):
            raise ValueError("Probabilities must be non-negative.")
        
        if sum(self._probabilities) != 1:
            raise ValueError("Sum of probabilities must be equal to 1.")
        
class AliasRandomGen(RandomGen):
    def __init__(
        self,
        random_nums: list[float],
        probabilities: list[float]
    ) -> None:
        
        self._random_nums = random_nums
        self._probabilities = probabilities

        self.verify_input_correctness()
    
        n = len(self._probabilities)
        avg = sum(self._probabilities) / n

        self._prob = [p * n for p in self._probabilities]
        self._alias = [-1] * n
        
        small = []
        large = []
    
        for i, p in enumerate(self._prob):
            if p < avg:
                small.append(i)
            else:
                large.append(i)
    
        while small and large:
            s = small.pop()
            l = large.pop()
            self._alias[s] = l
            self._prob[l] -= (avg - self._prob[s])
            if self._prob[l] < avg:
                small.append(l)
            else:
                large.append(l)
    
    def next_num(self) -> float:
        """  
        Returns one of the randomNums. When this method is called multiple 
        times over a long period, it should return the numbers roughly with 
        the initialized probabilities.  
        """

        n = len(self._random_nums)
        k = int(random.random() * n)

        if n == 0:
            return None

        if random.random() < self._prob[k]:
            return self._random_nums[k]
        else:
            return self._random_nums[self._alias[k]]

class CDFRandomGen(RandomGen):
    def __init__(
        self,
        random_nums: list[float],
        probabilities: list[float]
    ) -> None:
        
        self._random_nums = random_nums
        self._probabilities = probabilities
        self.verify_input_correctness()

        self._cdf = np.cumsum(probabilities)
    
    def next_num(self) -> float:
        """  
        Returns one of the randomNums. When this method is called multiple 
        times over a long period, it should return the numbers roughly with 
        the initialized probabilities.  
        """
        random_num = random.random()
        index = np.searchsorted(self._cdf, random_num)
        
        return self._random_nums[index]
    
class ExponentialRandomGen(RandomGen):
    def __init__(
        self,
        random_nums: list[float],
        probabilities: list[float]
    ) -> None:
        
        self._random_nums = random_nums
        self._probabilities = probabilities
        self.verify_input_correctness()
    
    def next_num(self) -> float:
        """  
        Returns one of the randomNums. When this method is called multiple 
        times over a long period, it should return the numbers roughly with 
        the initialized probabilities.  
        """
        random_num = random.random()
        probs = np.random.rand(len(self._random_nums)) / np.array(self._probabilities)
        index = np.argmin(probs)     
        return self._random_nums[index]
    

class LookupRandomGen(RandomGen):
    def __init__(
        self,
        random_nums: list[float],
        probabilities: list[float]
    ) -> None:
        
        self._random_nums = random_nums
        self._probabilities = probabilities
        self.verify_input_correctness()

        self._lookup_table = []
        max_dec_places = max(
            -Decimal(str(p)).normalize().as_tuple().exponent
            for p in self._probabilities if p > 0
        )
        scale = 10 ** max_dec_places

        self._lookup_table = []
        for num, prob in zip(self._random_nums, self._probabilities):
            count = round(prob * scale)
            if count > 0:
                self._lookup_table.extend([num] * count)

    def count_decimal_places(self, p: float, max_places: int = 9) -> int:
        s = format(p, 'f')
        if '.' in s:
            return min(len(s.split('.')[1].rstrip('0')), max_places)
        return 0

    def next_num(self) -> float:
        """  
        Returns one of the randomNums. When this method is called multiple 
        times over a long period, it should return the numbers roughly with 
        the initialized probabilities.  
        """
        random_num = random.random()
        index = min(int(random_num * len(self._lookup_table)), len(self._lookup_table) - 1)
        return self._lookup_table[index]