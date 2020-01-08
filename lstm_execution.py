import shutil

import pandas as pd

from utils.shared.lstm_hyper_parameters import lstm_hyper_parameters
from utils.shared.routes import *
from utils.shared.models.lstm_autoencoder import get_lstm_autoencoder_model
# from utils.shared.lstm_hyper_parameters import LSTM_WINDOW_SIZE, LSTM_ENCODING_DIMENSION, \
#   LSTM_THRESHOLD_FROM_TRAINING_PERCENT
from utils.shared.helper_methods import get_training_data_lstm, get_testing_data_lstm, anomaly_score_multi, \
    get_threshold, report_results, get_method_scores, is_excluded_flight, load_exclude_flights, \
    load_attacks, load_flight_routes

from tensorflow.python.keras.models import load_model
from sklearn.preprocessing import MaxAbsScaler
from utils.windows import windows
from collections import defaultdict
from datetime import datetime


def get_subdirectories(path):
    directories = []
    for directory in os.listdir(path):
        if os.path.isdir(os.path.join(path, directory)):
            directories.append(directory)
    return directories


def create_directories(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.makedirs(path)


def get_current_time():
    now = datetime.now()
    return now.strftime("%b-%d-%Y-%H-%M-%S")


def get_lstm_parameters():
    return  (lstm_hyper_parameters.get_window_size(),
            lstm_hyper_parameters.get_encoding_dimension(),
            lstm_hyper_parameters.get_activation(),
            lstm_hyper_parameters.get_loss(),
            lstm_hyper_parameters.get_optimizer(),
            lstm_hyper_parameters.get_threshold(),)


def run_model(training_data_path, test_data_path, results_path, similarity_score, save_model):
    print(get_lstm_parameters())

    window_size ,encoding_dimension ,activation ,loss ,optimizer ,threshold = get_lstm_parameters()

    # window_size = lstm_hyper_parameters.get_window_size()
    # encoding_dimension = lstm_hyper_parameters.get_encoding_dimension()
    # activation = lstm_hyper_parameters.get_activation()
    # loss = lstm_hyper_parameters.get_loss()
    # optimizer = lstm_hyper_parameters.get_optimizer()
    # threshold = lstm_hyper_parameters.get_threshold()

    FLIGHT_ROUTES = get_subdirectories(training_data_path)

    current_time = get_current_time()

    create_directories(f'{results_path}/lstm/{current_time}')

    for similarity in similarity_score:
        create_directories(f'{results_path}/lstm/{current_time}/{similarity}')

    for flight_route in FLIGHT_ROUTES:

        # check if scalar is necessary
        lstm, X_train, scalar = execute_train(flight_route,
                                              training_data_path=training_data_path,
                                              results_path=f'{results_path}/lstm/{current_time}',
                                              window_size=window_size,
                                              encoding_dimension=encoding_dimension,
                                              activation=activation,
                                              loss=loss,
                                              optimizer=optimizer,
                                              save_model=save_model)

        for similarity in similarity_score:

            tpr_scores, fpr_scores, delay_scores = execute_predict(flight_route,
                                                                    test_data_path = test_data_path,
                                                                    similarity_score = similarity,
                                                                    window_size = window_size,
                                                                    threshold = threshold,
                                                                    lstm = lstm,
                                                                    X_train = X_train,
                                                                    scalar = scalar)

            current_results_path = f'{results_path}/lstm/{current_time}/{similarity}/{flight_route}'
            create_directories(current_results_path)

            df = pd.DataFrame(tpr_scores)
            # df.to_csv(f'{results_path}{flight_route}/lstm/{similarity}/_tpr.csv', index=False)
            df.to_csv(f'{current_results_path}/{flight_route}_tpr.csv', index=False)

            df = pd.DataFrame(fpr_scores)
            # df.to_csv(f'{results_path}{flight_route}/lstm/{similarity}/_fpr.csv', index=False)
            df.to_csv(f'{current_results_path}/{flight_route}_fpr.csv', index=False)

            df = pd.DataFrame(delay_scores)
            # df.to_csv(f'{results_path}{flight_route}/lstm/{similarity}/_delay.csv', index=False)
            df.to_csv(f'{current_results_path}/{flight_route}_delay.csv', index=False)

            # report_results('export/results/lstm')

    ##################################################################


def execute_train(flight_route,
                  training_data_path=None,
                  results_path=None,
                  window_size=None,
                  encoding_dimension=None,
                  activation=None,
                  loss=None,
                  optimizer=None,
                  save_model=False):

    df_train = pd.read_csv(f'{training_data_path}/{flight_route}/without_anom.csv')

    df_train = df_train[
        ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']
    ]

    scalar = MaxAbsScaler()

    X_train = scalar.fit_transform(df_train)
    X_train = get_training_data_lstm(X_train, window_size)

    lstm = get_lstm_autoencoder_model(window_size, df_train.shape[1],
                                      encoding_dimension, activation, loss, optimizer)
    history = lstm.fit(X_train, X_train, epochs=10, verbose=1).history  # check if history is necessary
    if save_model:
        lstm.save(f'{results_path}/{flight_route}.h5')

    return lstm, X_train, scalar  # check if scalar is necessary


#####################################################
def execute_predict(flight_route,
                    test_data_path=None,
                    similarity_score=None,
                    window_size=None,
                    threshold=None,
                    lstm=None,
                    X_train=None,
                    scalar=None):
    tpr_scores = defaultdict(list)
    fpr_scores = defaultdict(list)
    delay_scores = defaultdict(list)

    X_pred = lstm.predict(X_train, verbose=1)
    scores_train = []
    for i, pred in enumerate(X_pred):
        scores_train.append(anomaly_score_multi(X_train[i], pred, similarity_score))

    # choose threshold for which <LSTM_THRESHOLD_FROM_TRAINING_PERCENT> % of training were lower
    THRESHOLD = get_threshold(scores_train, threshold)

    fligth_dir = os.path.join(test_data_path, flight_route)
    ATTACKS = get_subdirectories(fligth_dir)

    # csv_append = True

    for attack in ATTACKS:
        for flight_csv in os.listdir(f'{test_data_path}/{flight_route}/{attack}'):
            # if is_excluded_flight(flight_route, flight_csv):
            #     continue

            df_test = pd.read_csv(f'{test_data_path}/{flight_route}/{attack}/{flight_csv}')
            df_test_labels = df_test[['label']].values
            df_test = df_test[
                ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']]
            X_test = scalar.transform(df_test)
            X_test, y_test = get_testing_data_lstm(X_test, df_test_labels, window_size)

            X_pred = lstm.predict(X_test, verbose=1)
            scores_test = []
            for i, pred in enumerate(X_pred):
                scores_test.append(anomaly_score_multi(X_test[i], pred, similarity_score))

            predictions = [1 if x >= THRESHOLD else 0 for x in scores_test]

            method_scores = get_method_scores(predictions, "")

            # if csv_append:
            #     tpr_scores["csv file"].append(flight_csv)
            #     fpr_scores["csv file"].append(flight_csv)
            #     delay_scores["csv file"].append(flight_csv)

            tpr_scores[attack].append(method_scores[0])
            fpr_scores[attack].append(method_scores[1])
            delay_scores[attack].append(method_scores[2])

            csv_append = False

    return tpr_scores, fpr_scores, delay_scores

# ######################################################
# def execute(flight_route,
#             train=True,
#             add_plots=True,
#             training_data_path=None,
#             test_data_path=None,
#             results_path=None,
#             similarity_score=None,
#             window_size=None,
#             encoding_dimension=None,
#             activation=None,
#             loss=None,
#             optimizer=None,
#             threshold=None,
#             save_model=False):
#     # nab_scores = defaultdict(list)
#     tpr_scores = defaultdict(list)
#     fpr_scores = defaultdict(list)
#     delay_scores = defaultdict(list)
#
#     df_train = pd.read_csv(f'{training_data_path}/{flight_route}/without_anom.csv')
#
#     df_train = df_train[
#         ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']
#     ]
#
#     scalar = MaxAbsScaler()
#
#     X_train = scalar.fit_transform(df_train)
#     X_train = get_training_data_lstm(X_train, window_size)
#
#     if train:
#         lstm = get_lstm_autoencoder_model(window_size, df_train.shape[1],
#                                           encoding_dimension, activation, loss, optimizer)
#         history = lstm.fit(X_train, X_train, epochs=10, verbose=1).history
#         if save_model:
#             lstm.save(f'{results_path}/{flight_route}.h5')
#         # if add_plots:
#         #     plot(history['loss'], ylabel='loss', xlabel='epoch', title="Epoch Loss")
#     # else:
#     # lstm = load_model(f'export/models/lstm/model_{flight_route}.h5')
#
#     X_pred = lstm.predict(X_train, verbose=1)
#     scores_train = []
#     for i, pred in enumerate(X_pred):
#         scores_train.append(anomaly_score_multi(X_train[i], pred, similarity_score))
#
#     # choose threshold for which <LSTM_THRESHOLD_FROM_TRAINING_PERCENT> % of training were lower
#     THRESHOLD = get_threshold(scores_train, threshold)
#
#     fligth_dir = os.path.join(test_data_path, flight_route)
#     ATTACKS = get_subdirectories(fligth_dir)
#
#     for attack in ATTACKS:
#         for flight_csv in os.listdir(f'{test_data_path}/{flight_route}/{attack}'):
#             # if is_excluded_flight(flight_route, flight_csv):
#             #     continue
#
#             df_test = pd.read_csv(f'{test_data_path}/{flight_route}/{attack}/{flight_csv}')
#             df_test_labels = df_test[['label']].values
#             df_test = df_test[
#                 ['Direction', 'Speed', 'Altitude', 'lat', 'long', 'first_dis', 'second_dis', 'third_dis', 'fourth_dis']]
#             X_test = scalar.transform(df_test)
#             X_test, y_test = get_testing_data_lstm(X_test, df_test_labels, window_size)
#
#             X_pred = lstm.predict(X_test, verbose=1)
#             scores_test = []
#             for i, pred in enumerate(X_pred):
#                 scores_test.append(anomaly_score_multi(X_test[i], pred, similarity_score))
#
#             # if add_plots:
#             #     plot_reconstruction_error_scatter(scores=scores_train, labels=[0] * len(scores_train),
#             #                                       threshold=THRESHOLD, title=f'Outlier Score Training ({attack})')
#             #     plot_reconstruction_error_scatter(scores=scores_test, labels=y_test, threshold=THRESHOLD,
#             #                                       title=f'Outlier Score Testing ({attack})')
#
#             predictions = [1 if x >= THRESHOLD else 0 for x in scores_test]
#
#             # nab_scores[attack].append(get_nab_score(predictions, windows=windows["flight_lstm"]))
#             # previous_method_scores = get_method_scores(predictions, windows=windows["flight_lstm"])
#             method_scores = get_method_scores(predictions, "")
#
#             tpr_scores["csv file number"].append(flight_csv)
#             fpr_scores["csv file number"].append(flight_csv)
#             delay_scores["csv file number"].append(flight_csv)
#
#             tpr_scores[attack].append(method_scores[0])
#             fpr_scores[attack].append(method_scores[1])
#             delay_scores[attack].append(method_scores[2])
#
#     return tpr_scores, fpr_scores, delay_scores  # nab_scores,
