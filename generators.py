import random

class UniformGenerator:
    def __init__(self, seed):
        random.seed(seed)  

    def uniformGenerator(self):
        return random.uniform(5, 50)

class GaussianGenerator:
    def __init__(self, seed):
        random.seed(seed) 

    def gaussianGenerator(self):
        return random.gauss(0, 4) 


class ExponentialGenerator:
    def __init__(self, seed, lambd):
        self.lambda_value = lambd
        random.seed(seed) 

    def exponentialGenerator(self):
        return random.expovariate(self.lambda_value)




