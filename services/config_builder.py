def build_training_config(request):
    return {
        "model": request.model_name_or_path,
        "data": {
            "collection": request.data_config.collection,
            "script": request.data_config.process_script,
            "dataset_class": request.data_config.dataset_class
        },
        "training": {
            "method": request.training_config.method,
            "arguments": request.training_config.training_arguments.dict(),
            "algorithm": request.training_config.algorithm,
            "reward_fn": request.training_config.scoring_script,
            "reward_class": request.training_config.scoring_class,
        },
        "output": request.output_config.dict()
    }