import memory_profiler
import time

def check_even_normal(numbers):
    even = []
    for num in numbers:
        if num % 2 == 0: 
            even.append(num**3)
            
    return even

def check_even_generator(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num**3



if __name__ == '__main__':
    
    m1 = memory_profiler.memory_usage()
    t1 = time.clock()
    cubes = check_even_normal(range(1000000))
    t2 = time.clock()
    m2 = memory_profiler.memory_usage()
    time_diff = t2 - t1
    mem_diff = m2[0] - m1[0]
    print(f"It took {time_diff} Secs and {mem_diff} Mb to execute this method")

    m3 = memory_profiler.memory_usage()
    t1 = time.clock()
    cubes = check_even_generator(range(1000000))
    t2 = time.clock()
    m4 = memory_profiler.memory_usage()
    time_diff = t2 - t1
    mem_diff = m4[0] - m3[0]
    print(f"It took {time_diff} Secs and {mem_diff} Mb to execute this method")
    