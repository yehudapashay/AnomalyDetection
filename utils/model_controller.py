'''
Anomaly Detection of GPS Spoofing Attacks on UAVs
Authors: Lior Pizman & Yehuda Pashay
GitHub: https://github.com/liorpizman/AnomalyDetection
DataSets: 1. ADS-B dataset 2. simulated data
---
Controller which mapping all the actions between the setting in the input and the user interface
'''

from utils.input_settings import InputSettings
from utils.models_execution import ModelsExecution


class ModelController:
    """
     A Class used to map all the actions in the system


     Methods
     -------
    set_training_data_path(directory)
            Description | Set the path of the train data set directory

    get_training_data_path()
            Description | Get the path of the train data set directory

    set_test_data_path(directory)
            Description | Set the path of the test data set directory

    get_test_data_path()
            Description | Get the path of the test data set directory

    set_results_path(directory)
            Description | Set the path of the results directory

    get_results_path()
            Description | Get the path of the results directory

    set_algorithm_parameters(algorithm_name, algorithm_parameters)
            Description | Set the parameters which were chosen by the user to a given algorithm

    remove_algorithm_parameters(algorithm_name, algorithm_parameters)
            Description | Remove the values of the parameters which were chosen by the user to a given algorithm

    set_similarity_score(similarity_list)
            Description | Set the list of all chosen similarity function by the user

    set_saving_model(save_model)
            Description | Set the variable which indicates whether the user want to save the current model or not

    run_models()
            Description | Execute models creation/loading process

    set_new_model_running(new_model_running)
            Description | Set the variable which indicates whether the user chose to create new model or to load an
                          existing model

    set_existing_algorithms(algorithms_dict)
            Description | Set a dictionary which includes all the algorithm which were chosen by the user in a load
                          existing models flow

    set_features_columns_options()
            Description | Set the data set columns which were loaded from the test data set

    get_features_columns_options()
            Description | Get the data set columns which were loaded from the test data set

    set_users_selected_features(algorithm_name, features_list)
            Description | Set the data set columns which were selected by the user for a given algorithm

    add_new_thread(new_thread)
            Description | Add new running thread to the system

    get_existing_thread()
            Description | Get running thread

    get_new_model_running()
            Description | Indicator whether the user chose a new model creation flow or not

    get_algorithms()
            Description | Get all the algorithms

    remove_algorithm(algorithm_name)
            Description | Remove a given algorithm

    set_results_selected_algorithm(selected_algorithm)
            Description | Set the variable which indicates which algorithm should be shown in the results table
                          at this moment

    set_results_selected_flight_route(selected_flight_route)
            Description | Set the variable which indicates which flight route should be shown in the results table
                          at this moment

    get_results_selected_algorithm()
            Description | Get the variable which indicates which algorithm should be shown in the results table
                          at this moment

    get_results_selected_flight_route()
            Description | Get the variable which indicates which flight route should be shown in the results table
                          at this moment

    reset_input_settings_params()
            Description | Reset all the values of input settings attributes

    get_flight_routes()
            Description | Get all the flight routes in the test set

    get_existing_algorithms()
            Description | Get a dictionary which includes all the algorithm which were chosen by the user in a load
                          existing models flow

     """

    def __init__(self, gui_controller):
        """
        Parameters
        ----------
        gui_controller : AnomalyDetectionGUI
            The controller which maps all the actions in UI
        """
        self.gui_controller = gui_controller

    def set_training_data_path(self, directory):
        InputSettings.set_training_data_path(directory)

    def get_training_data_path(self):
        return InputSettings.get_training_data_path()

    def set_test_data_path(self, directory):
        InputSettings.set_test_data_path(directory)

    def get_test_data_path(self):
        return InputSettings.get_test_data_path()

    def set_results_path(self, directory):
        InputSettings.set_results_path(directory)

    def get_results_path(self):
        return InputSettings.get_results_path()

    def set_algorithm_parameters(self, algorithm_name, algorithm_parameters):
        InputSettings.set_algorithm_parameters(algorithm_name, algorithm_parameters)

    def remove_algorithm_parameters(self, algorithm_name, algorithm_parameters):
        InputSettings.remove_algorithm_parameters(algorithm_name, algorithm_parameters)

    def set_similarity_score(self, similarity_list):
        InputSettings.set_similarity_score(similarity_list)

    def set_saving_model(self, save_model):
        InputSettings.set_saving_model(save_model)

    def run_models(self):
        ModelsExecution.run_models()

    def set_new_model_running(self, new_model_running):
        InputSettings.set_new_model_running(new_model_running)

    def set_existing_algorithms(self, algorithms_dict):
        InputSettings.set_existing_algorithms(algorithms_dict)

    def set_features_columns_options(self):
        InputSettings.set_features_columns_options()

    def get_features_columns_options(self):
        return InputSettings.get_features_columns_options()

    def set_users_selected_features(self, algorithm_name, features_list):
        InputSettings.set_users_selected_features(algorithm_name, features_list)

    def add_new_thread(self, new_thread):
        InputSettings.add_new_thread(new_thread)

    def get_existing_thread(self):
        return InputSettings.get_existing_thread()

    def get_new_model_running(self):
        return InputSettings.get_new_model_running()

    def get_algorithms(self):
        return InputSettings.get_algorithms()

    def remove_algorithm(self, algorithm_name):
        InputSettings.remove_algorithm(algorithm_name)

    def set_results_selected_algorithm(self, selected_algorithm):
        InputSettings.set_results_selected_algorithm(selected_algorithm)

    def set_results_selected_flight_route(self, selected_flight_route):
        InputSettings.set_results_selected_flight_route(selected_flight_route)

    def get_results_selected_algorithm(self):
        return InputSettings.get_results_selected_algorithm()

    def get_results_selected_flight_route(self):
        return InputSettings.get_results_selected_flight_route()

    def reset_input_settings_params(self):
        InputSettings.reset_input_settings_params()

    def get_flight_routes(self):
        return InputSettings.get_flight_routes()

    def get_existing_algorithms(self):
        return InputSettings.get_existing_algorithms()
