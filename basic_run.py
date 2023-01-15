from niaautoarm import AutoARM
from niaarm.dataset import Dataset
from niapy.algorithms.basic import ParticleSwarmAlgorithm, DifferentialEvolution
from niapy.task import Task, OptimizationType

# load dataset from csv
data = Dataset("datasets/Abalone.csv")

# set dimension of the problem
# components = preprocessing (1) + algorithm (1) + hyperparameters (2 (NP,FES)) +
# metrics (8, (support, confidence, lift, coverage, amplitude, inclusion, comprehensibility))
dimension = 11  # can be extended when new components are added

# define which preprocessing methods to use
# TODO | No preprocessing techniques implemented for now
preprocessing = ["FeatureSelection", "HotCodeEncoding", "Squashing"]

# feature selection algorithms
# TODO
fs = ["jDEFSTH", "PCA"]

# define algorithms for searching the association rules
algorithms = ["PSO", "DE", "GA", "FA"]

# define hyperparameters and their min/max values
hyperparameter1 = {
    "parameter": "NP",
    "min": 5,
    "max": 75
}

hyperparameter2 = {
    "parameter": "N_FES",
    "min": 5000,
    "max": 25000
}
# create array
hyperparameters = [hyperparameter1, hyperparameter2]

# evaluation criteria
metrics = ["support", "confidence", "coverage", "amplitude", "inclusion", "comprehensibility"]

# Create a problem:::

problem = AutoARM(data, preprocessing, algorithms, hyperparameters, metrics, logging=True)

# build niapy task
task = Task(
    problem=problem,
    max_iters=1000,
    optimization_type=OptimizationType.MAXIMIZATION)

# use Differential Evolution (DE) algorithm
# see full list of available algorithms: https://github.com/NiaOrg/NiaPy/blob/master/Algorithms.md
algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)

# use Particle swarm Optimization (PSO) algorithm from NiaPy library
algo2 = ParticleSwarmAlgorithm(
    population_size=100,
    min_velocity=-4.0,
    max_velocity=4.0)

# run algorithm
best = algo.run(task=task)
