from gui.shared.helper_methods import read_json_file, get_model_path
from models.lstm.lstm_execution import run_model
from utils.input_settings import InputSettings


class ModelsExecution:

    @classmethod
    def get_new_model_parameters(cls):
        return (InputSettings.get_training_data_path(),
                InputSettings.get_saving_model(),
                InputSettings.get_algorithms(),
                None,
                InputSettings.get_users_selected_features(),)

    @classmethod
    def get_load_model_parameters(cls):
        return (None,
                False,
                InputSettings.get_existing_algorithms(),
                InputSettings.get_existing_algorithms_threshold(),)

    @classmethod
    def get_parameters(cls):
        return (InputSettings.get_similarity(),
                InputSettings.get_test_data_path(),
                InputSettings.get_results_path(),
                InputSettings.get_new_model_running(),)

    @staticmethod
    def run_models():
        similarity_score, test_data_path, results_path, new_model_running = ModelsExecution.get_parameters()

        if new_model_running:
            training_data_path, save_model, algorithms, threshold, features_list = ModelsExecution.get_new_model_parameters()
        else:
            training_data_path, save_model, algorithms, threshold = ModelsExecution.get_load_model_parameters()

        for algorithm in algorithms:
            if new_model_running:
                algorithm_model_path = None
            else:
                algorithm_path = InputSettings.get_existing_algorithm_path(algorithm)
                features_list = read_json_file(f'{algorithm_path}/model_data.json')['features']
                algorithm_model_path = get_model_path(algorithm_path)
            model_execution_function = getattr(ModelsExecution, algorithm + "_execution")
            model_execution_function(test_data_path,
                                     results_path,
                                     similarity_score,
                                     training_data_path,
                                     save_model,
                                     new_model_running,
                                     algorithm_model_path,
                                     threshold,
                                     features_list)

    @staticmethod
    def LSTM_execution(test_data_path,
                       results_path,
                       similarity_score,
                       training_data_path,
                       save_model,
                       new_model_running,
                       algorithm_path,
                       threshold,
                       features_list):
        run_model(training_data_path,
                  test_data_path,
                  results_path,
                  similarity_score,
                  save_model,
                  new_model_running,
                  algorithm_path,
                  threshold,
                  features_list)
