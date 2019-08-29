#Requires Python 3 for "perf_counter" function in the "time" module
import functools;
import time;

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter() * 1000; #In miliseconds
        funcReturn = func(*args, **kwargs);
        stop_time = time.perf_counter() * 1000;
        run_time = stop_time - start_time;
        print("{} took {:.4f} miliseconds to complete".format(func.__name__, run_time));
        return funcReturn;
    return wrapper;


@timer
def doRecursiveFib(num):
    def getFib(num):
        if(num <= 0):
            return 0;
        elif(num == 1):
            return 1;
        return getFib(num-1) + getFib(num-2);
    return getFib(num);


@timer
def doMemoizeFib(num):
    cache = {};
    def getMemoizeFib(num):
        if(num <= 0):
            return 0;
        elif(num == 1):
            return 1;
        elif(num not in cache):
            cache[num] = getMemoizeFib(num-2) + getMemoizeFib(num-1);
        return cache[num];
    return getMemoizeFib(num);


def memoize(func):
    cache = {};
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs);
        if(key not in cache): 
            cache[key] = func(*args, **kwargs);
        return cache[key];
    return wrapper;


@timer
def doMemoizeDecoratorFib(num):
    @memoize
    def getFib2(num):
        if(num <= 0):
            return 0;
        elif(num == 1):
            return 1;
        return getFib2(num-1) + getFib2(num-2);
    return getFib2(num);


class Memoize:
    def __init__(self, func):
        self.func = func;
        self.cache = {};

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs);
        if(key not in self.cache):
            self.cache[key] = self.func(*args, **kwargs);
        return self.cache[key];
 

def doMemoizeClassFib(num):
    start_time = time.perf_counter() * 1000; #In miliseconds
    @Memoize
    def getFib3(num):
        if(num <= 0):
            return 0;
        elif(num == 1):
            return 1;
        return getFib3(num-1) + getFib3(num-2);
    value = getFib3(num);
    stop_time = time.perf_counter() * 1000;
    run_time = stop_time - start_time;
    print("{} took {:.4f} miliseconds to complete".format("doMemoizeClassFib", run_time));
    return value;


def doUntimedMemoizeFib(num):
    cache = {};
    def getMemoizeFib(num):
        if(num <= 0):
            return 0;
        elif(num == 1):
            return 1;
        elif(num not in cache):
            cache[num] = getMemoizeFib(num-2) + getMemoizeFib(num-1);
        return cache[num];
    return getMemoizeFib(num);


def askForNumInput():
    num = 0;
    while(num <= 0):
        num = int(input("Which fibonnacci number do you want to calculate: "));
    return num;


def displayResults(fibNum, isFullResult):
    if(isFullResult == "y" or  isFullResult == "yes"):
        print("\nTime needed for each function to calculate the anwser");
        print("-"*60);
        doRecursiveFib(fibNum);
        doMemoizeFib(fibNum);
        doMemoizeDecoratorFib(fibNum);
        doMemoizeClassFib(fibNum);

    anwser = doUntimedMemoizeFib(fibNum);
    print("---------------Anwser: {}---------------".format(anwser));


def askFibonnaciNumber():
    askAgain = "y";
    while(askAgain == "y" or askAgain == "yes"):
        fibNum = askForNumInput();
        isFullResult = input("Display speed performance results(y/n)? ").lower();
        displayResults(fibNum, isFullResult)
        askAgain = input("\nHave another number(y/n)? ").lower();
        print("");
       

askFibonnaciNumber();
