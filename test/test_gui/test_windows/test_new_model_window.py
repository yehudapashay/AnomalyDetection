'''
Anomaly Detection of GPS Spoofing Attacks on UAVs
Authors: Lior Pizman & Yehuda Pashay
GitHub: https://github.com/liorpizman/AnomalyDetection
DataSets: 1. ADS-B dataset 2. simulated data
---
Tests for new model window
'''

import unittest

from tkinter import END
from unittest.mock import MagicMock
from gui.gui_controller import AnomalyDetectionGUI
from utils.input_settings import InputSettings


class TestNewModelWindow(unittest.TestCase):

    def setUp(self):
        """
        Set up values before test
        :return:
        """

        self.app = AnomalyDetectionGUI()
        self.new_model_window = self.app.frames["NewModel"]

        self.new_model_window.training_input.delete(0, END)
        self.new_model_window.test_input.delete(0, END)
        self.new_model_window.results_input.delete(0, END)

        self.new_model_window.training_input.insert(0, 'path_a')
        self.new_model_window.test_input.insert(0, 'path_b')
        self.new_model_window.results_input.insert(0, 'path_c')

    def test_set_new_model_parameters(self):
        """
        Test valid inputs for each path
        :return:
        """

        self.app.set_features_columns_options = MagicMock(return_value={})
        self.new_model_window.set_new_model_parameters()
        self.assertEqual(self.new_model_window.training_input.get(), InputSettings.get_training_data_path())
        self.assertEqual(self.new_model_window.test_input.get(), InputSettings.get_test_data_path())
        self.assertEqual(self.new_model_window.results_input.get(), InputSettings.get_results_path())


if __name__ == '__main__':
    unittest.main()
