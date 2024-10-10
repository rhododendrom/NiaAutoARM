# Description: This is a basic example of how to run the ARMPipelineOptimizer class.
from niaarm.dataset import Dataset
from niaautoarm.armoptimizer import AutoARMOptimizer
from niapy.algorithms.basic import ParticleSwarmOptimization, DifferentialEvolution, GeneticAlgorithm, FireflyAlgorithm
from niapy.algorithms.basic.ga import uniform_crossover, uniform_mutation

if __name__ == "__main__":        

    # load dataset from csv
    data = Dataset("datasets/Abalone.csv")

    # define which preprocessing methods to use
    preprocessing = ["min_max_scaling", "squash_cosine", "none"]

    # define algorithms for searching the association rules
    algorithms = [ParticleSwarmOptimization(min_velocity=-4, max_velocity=4),
                    DifferentialEvolution(crossover_probability=0.9, differential_weight=0.5),
                    GeneticAlgorithm(crossover=uniform_crossover, mutation=uniform_mutation, crossover_rate=0.9, mutation_rate=0.1), 
                    FireflyAlgorithm(alpha=1.0, beta0=0.2, gamma=1.0)]

    # define hyperparameters and their min/max values
    hyperparameter1 = {
        "parameter": "NP",
        "min": 5,
        "max": 15
    }

    hyperparameter2 = {
        "parameter": "N_FES",
        "min": 1000,
        "max": 2000
    }
    # create array
    hyperparameters = [hyperparameter1, hyperparameter2]

    # evaluation criteria
    metrics = [
        "support",
        "confidence",
        "coverage",
        "amplitude",
        "inclusion",
        "comprehensibility"]    

    pipeline_optimizer = AutoARMOptimizer(data=data, 
                                feature_prepocessing_techniques=preprocessing,
                                rule_mining_algorithms=algorithms, 
                                metrics=metrics,
                                hyperparameters=hyperparameters,
                                log=True,
                                log_verbose=True,
                                log_output_file=None
                                )
    
    pipeline_optimizer.run(
        optimization_algorithm="ParticleSwarmAlgorithm",
        population_size=5,
        max_iters=2,
        optimize_metric_weights=True,
        allow_multiple_preprocessing=False,
        output_pipeline_file="results.pckl")