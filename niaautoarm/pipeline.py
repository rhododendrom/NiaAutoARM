class Pipeline:
    r"""Class representing a pipeline.
    Args:
       preprocessing (str): Selected preprocessing techniques.
       algorithm (str): Selected algorithm.
       metrics (list): Selected metrics.
       parameters (list): Hyperparameter values.
       support (float): Support value.
       confidence (float): Confidence value.
    """

    def __init__(self, preprocessing, algorithm, metrics, parameters, fitness, rules):
        self.preprocessing = preprocessing
        self.algorithm = algorithm
        self.metrics = metrics
        self.parameters = parameters
        self.fitness = fitness
        self.rules = rules
        self.support = rules.mean("support")            
        self.confidence = rules.mean("confidence")
        self.num_rules = len(rules)


    def __str__(self):
        return "\nPreprocessing: {}\nAlgorithm: {}\nHyperparameters: {}\nMetrics: {}\nFitness: {:.4f}\nMean Support: {:.4f}\nMean Confidence: {:.4f}\n# rules: {}\n------------------".format(
            self.preprocessing, self.algorithm, self.parameters, self.metrics, self.fitness, self.support, self.confidence, self.num_rules)
    
