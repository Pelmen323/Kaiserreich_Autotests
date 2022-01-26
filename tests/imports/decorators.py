from timeit import default_timer as timer


def util_decorator(func):
    """To be used with tests that receive false_positives arg

    Adds intro message and timer functionality"""
    def inner(filepath, false_positives):
        print("The test is started. Please wait...")
        start = timer()
        func(filepath, false_positives)
        end = timer()
        print(f"The test is finished in {round(end-start, 3)} seconds!")

    return inner


def util_decorator_no_false_positives(func):
    """To be used with tests that receive only filepath arg

    Adds intro message and timer functionality"""
    def inner(filepath):
        print("The test is started. Please wait...")
        start = timer()
        func(filepath)
        end = timer()
        print(f"The test is finished in {round(end-start, 3)} seconds!")

    return inner
