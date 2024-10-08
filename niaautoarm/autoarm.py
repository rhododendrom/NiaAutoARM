import numpy as np
from niaarm import NiaARM, squash
from niapy.problems import Problem
from niapy.task import Task, OptimizationType

from niaautoarm.pipeline import Pipeline
from niaautoarm.preprocessing_class import Preprocessing

def float_to_category(component, val):
    r"""Map float value to component (category). """
    if val == 1:
        return len(component) - 1
    return int(val * len(component))


def float_to_num(component, val):
    r"""Map float value to integer. """
    parameters = [1] * len(component)
    for i in range(len(component)):
        parameters[i] = int(int(component[i]['min'] + (int(component[i]['max']) - int(component[i]['min'])) * val[i]))
    return parameters


def threshold(component, val):
    r"""Calculate whether feature is over a threshold. """
    selected = [c for i, c in enumerate(component) if val[i] > 0.5]
    return tuple(selected)

def calculate_dimension_of_the_problem(
        preprocessing,
        algorithms,
        hyperparameters,
        metrics):
    return ( 2 + len(hyperparameters) + len(metrics))


class AutoARM(Problem):
    r"""Definition of Auto Association Rule Mining.

    The implementation is composed of ideas found in the following papers:
    * Pečnik, L., Fister, I., & Fister, I. (2021). NiaAML2: An Improved AutoML Using Nature-Inspired Algorithms. In Advances in Swarm Intelligence: 12th International Conference, ICSI 2021, Qingdao, China, July 17–21, 2021, Proceedings, Part II 12 (pp. 243-252). Springer International Publishing.

    * Stupan, Ž., & Fister, I. (2022). NiaARM: A minimalistic framework for Numerical Association Rule Mining. Journal of Open Source Software, 7(77), 4448.

    Args:
        dataset (list): The entire dataset.
        preprocessing (list): Preprocessing components (data squashing or none).
        algorithms (list): Algorithm components (one arbitrary algorithm from niapy collection).
        hyperparameters (list): Selected hyperparameter values.
        metrics (list): Metrics component.
        logging (bool): Enable logging of fitness improvements. Default: ``False``.
    Attributes:
        rules (RuleList): A list of mined association rules.
    """

    def __init__(
            self,
            dataset,
            preprocessing,
            algorithms,
            hyperparameters,
            metrics,
            logger
    ):
        r"""Initialize instance of AutoARM.dataset_class

        Arguments:

        """
        # calculate the dimension of the problem
        dimension = calculate_dimension_of_the_problem(
            preprocessing, algorithms, hyperparameters, metrics)

        super().__init__(dimension, 0, 1)
        self.preprocessing = preprocessing
        self.algorithms = algorithms
        self.hyperparameters = hyperparameters
        self.metrics = metrics
        self.best_fitness = -np.inf
        self.preprocessing_instance = Preprocessing(dataset,None)

        self.logger = logger
        self.all_pipelines = []
        self.best_pipeline = None

    def get_best_pipeline(self):
        return self.best_pipeline

    def get_all_pipelines(self):
        return self.all_pipelines

    def _evaluate(self, x):
        # get preprocessing components (just one atm)
        preprocessing_component = self.preprocessing[float_to_category(
            self.preprocessing, x[0])]

        #get the algorithm component
        algorithm_component = self.algorithms[float_to_category(
            self.algorithms, x[1])]

        hyperparameter_component = float_to_num(self.hyperparameters, x[2:4])

        metrics_component = threshold(self.metrics, x[4:])

        if metrics_component == ():  # if no metrics are selected TODO: check for alternative solution
            return -np.inf

        self.preprocessing_instance.set_preprocessing_algorithms([preprocessing_component]) #TODO can be a list of multiple preprocessing techniques, order is determined by importance in class
        dataset = self.preprocessing_instance.apply_preprocessing()

        problem = NiaARM(
            dataset.dimension,            
            dataset.features,
            dataset.transactions,
            metrics=metrics_component)        

        # build niapy task
        task = Task(
            problem=problem,
            max_evals=hyperparameter_component[1],
            optimization_type=OptimizationType.MAXIMIZATION)

        algorithm_component.NP = hyperparameter_component[0]
        
        _, fitness = algorithm_component.run(task=task)

        if (len(problem.rules) == 0):
            return -np.inf

        pipeline = Pipeline(preprocessing_component, algorithm_component.Name[1], metrics_component, hyperparameter_component, fitness, problem.rules)

        # store each generated and valid pipeline in a list for post-processing
        self.all_pipelines.append(pipeline)
        
        if fitness >= self.best_fitness:

            self.best_fitness = fitness
            self.best_pipeline = pipeline

            if self.logger is not None:
                self.logger.log_pipeline(pipeline)
        else:
            print("Fitness: ", fitness)
        return fitness
