import time

import matplotlib.pyplot as plt

from pympler import asizeof

from weighted_random_sampling import AliasRandomGen, CDFRandomGen, ExponentialRandomGen, LookupRandomGen


def time_sampling_method(method, *args):
    """
    Measure the time taken to sample from a method.
    """
    start_time = time.time()
    for _ in range(100000):
        method(*args)
    return time.time() - start_time

def time_setup(constructor, *args):
    """
    Measure the time taken to set up an instance of a class.
    """
    start = time.time()
    instance = constructor(*args)
    return instance, time.time() - start

def measure_memory_usage(method):
    """
    Measure the memory usage of a method.
    """
    return asizeof.asizeof(method)

def run_profiling():
    """
    Run the profiling for different random number generators and plot the results.
    """

    input_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000]
    classes = [AliasRandomGen, CDFRandomGen, LookupRandomGen]
    setup_times = {cls.__name__: [] for cls in classes}
    sampling_times = {cls.__name__: [] for cls in classes}
    memory_usages = {cls.__name__: [] for cls in classes}

    for size in input_sizes:
        random_nums = [i for i in range(size)]
        probabilities = [1 / size] * size 

        for cls in classes:
            instance, setup_time = time_setup(cls, random_nums, probabilities)
            sampling_time = time_sampling_method(instance.next_num)

            setup_times[cls.__name__].append(setup_time)
            sampling_times[cls.__name__].append(sampling_time)
            memory_usages[cls.__name__].append(measure_memory_usage(instance))

    # Plot the results
    plt.figure(figsize=(12, 8))

    # Setup time plot
    plt.subplot(3, 1, 1)
    for method in setup_times:
        plt.plot(input_sizes, setup_times[method], label=method)
    plt.xlabel('Input Size')
    plt.ylabel('Setup Time (seconds)')
    plt.title('Setup Time vs. Input Size')
    plt.legend()

    # Sampling time plot
    plt.subplot(3, 1, 2)
    for method in sampling_times:
        plt.plot(input_sizes, sampling_times[method], label=method)
    plt.xlabel('Input Size')
    plt.ylabel('Sampling Time (seconds per sample)')
    plt.title('Sampling Time vs. Input Size')
    plt.legend()

    # Memory usage plot
    plt.subplot(3, 1, 3)
    for method in memory_usages:
        plt.plot(input_sizes, memory_usages[method], label=method)
    plt.xlabel('Input Size')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Memory Usage vs. Input Size')
    plt.legend()

    plt.tight_layout()
    plt.show()

    plt.savefig('plots/profiling_results.png')

if __name__ == "__main__":
    run_profiling()
