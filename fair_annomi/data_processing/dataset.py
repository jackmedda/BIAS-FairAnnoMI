import os
from typing import Iterable

import numpy as np
import pandas as pd
import sklearn as sk
import sklearn_pandas as sk_pd

from .utils import replace_substr_column_dataframe, clean_utterance_text


class AnnoMI(object):

    _DEFAULT_DATA_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.pardir, 'data'
    )

    _DEFAULT_DATASET_PATH = os.path.join(_DEFAULT_DATA_PATH, 'dataset.csv')
    _DEFAULT_TOPICS_MAP_PATH = os.path.join(_DEFAULT_DATA_PATH, 'new_topics_distribution.csv')

    def __init__(self, dataset_path='', **kwargs):
        self.dataset_path = dataset_path or self._DEFAULT_DATASET_PATH
        self.dataset = pd.read_csv(self.dataset_path)

        self._topic_field = kwargs.get('topic_field', 'topic')
        self._topic_sep = kwargs.get('topic_sep', '|')

        self._cleaned = False

        self.topic_map = None
        self._old_topic_field = kwargs.get('old_topic_field', 'old_topic')
        self._new_topic_field = kwargs.get('new_topic_field', 'new_topic')
        self._utterance_text_field = kwargs.get('utterance_text_field', 'utterance_text')

    def clean_topics(self, dataset=None):
        """
        Original dataset contains both 'smoking cessation' and 'smoking cessation '. They will be merged into
        'smoking cessation'.
        :return:
        """
        dataset = self.dataset.copy() if dataset is None else dataset
        possible_unique_topics = dataset[self._topic_field].str.strip().unique()
        partial_unique_topics = dataset[self._topic_field].unique()

        # If False the cleaning of the topics has already been done
        if possible_unique_topics.shape[0] != partial_unique_topics.shape[0]:
            self._cleaned = True

            unique_topics, topic_counts = np.unique(
                np.concatenate((possible_unique_topics, partial_unique_topics)),
                return_counts=True
            )
            clean_topic_map = dict(zip(
                unique_topics[topic_counts == 1],
                map(str.strip, unique_topics[topic_counts == 1])
            ))

            clean_topic_map.update(dict(zip(possible_unique_topics, possible_unique_topics)))

            dataset[self._topic_field] = dataset[self._topic_field].map(clean_topic_map)

        return dataset

    def remap_topics(self, dataset=None):
        if not self._cleaned:
            print('`clean_topics` should be called before remapping the topics')
        else:
            dataset = self.dataset.copy() if dataset is None else dataset

            if self.topic_map is None:
                self.topic_map = pd.read_csv(self._DEFAULT_TOPICS_MAP_PATH)

            topic_dict_map = dict(self.topic_map[[self._old_topic_field, self._new_topic_field]].to_numpy())
            dataset[self._topic_field] = dataset[self._topic_field].map(
                lambda x: topic_dict_map.get(
                    x,
                    self._topic_sep.join(map(topic_dict_map.get, x.split(self._topic_sep))) if self._topic_sep in x else None
                )
            )

            return dataset.dropna(subset=[self._topic_field])

    def replace_abbreviations(self, dataset=None, mapping=None):
        dataset = self.dataset.copy() if dataset is None else dataset
        return replace_substr_column_dataframe(dataset, self._utterance_text_field, mapping=mapping, inplace=False)

    def clean_utterance_text(self, dataset=None):
        dataset = self.dataset.copy() if dataset is None else dataset
        return clean_utterance_text(dataset, self._utterance_text_field, inplace=False)

    def text_lowercase(self, dataset=None):
        dataset = self.dataset.copy() if dataset is None else dataset
        dataset[self._utterance_text_field] = dataset[self._utterance_text_field].str.lower()
        return dataset

    def unprocessed_dataset(self):
        dataset = self.clean_topics()
        return self.remap_topics(dataset=dataset)

    def processed_dataset(self):
        dataset = self.unprocessed_dataset()
        dataset = self.replace_abbreviations(dataset=dataset)
        dataset = self.clean_utterance_text(dataset=dataset)
        return self.text_lowercase(dataset=dataset)

    def train_test_split(self, target_cols=None, test_size=0.2, encode_target=True):
        target_cols = ['client_talk_type', 'main_therapist_behaviour'] if target_cols is None else target_cols
        target_cols = [target_cols] if not isinstance(target_cols, Iterable) else target_cols
        train, test = [], []
        encoders = dict.fromkeys(target_cols)
        for t_col in target_cols:
            tr, te, encoder = self.train_test_split_target_topic_distributed(t_col, test_size=test_size, encode_target=encode_target)
            encoders[t_col] = encoder
            train.append(tr)
            test.append(te)

        return pd.concat(train), pd.concat(test),

    def train_test_split_target_topic_distributed(self,
                                                  dataset=None,
                                                  target_col='client_talk_type',
                                                  test_size=0.2,
                                                  shuffle=True,
                                                  as_xy=False,
                                                  encode_target=True,
                                                  handle_multi_topic=True):
        encoder = None
        train, test = [], []
        train_size = 1 - test_size
        dataset = self.dataset if dataset is None else dataset
        if encode_target:
            mapper = sk_pd.DataFrameMapper([
                (target_col, sk.preprocessing.LabelEncoder())
            ])
            dataset[target_col] = mapper.fit_transform(dataset)
            encoder = mapper.built_features[0][1]

        target_topic_gby = dataset.groupby([target_col, self._topic_field])
        for target, topic in list(target_topic_gby.groups.keys()):
            df = target_topic_gby.get_group((target, topic))
            if shuffle:
                random_sample = df.sample(frac=1)
            if random_sample.shape[0] < 2:
                if handle_multi_topic:
                    multi_topics = topic.split(self._topic_sep)
                    topic_flag = False
                    for t in multi_topics:
                        if target_topic_gby.get_group((target, t)).shape[0] >= 2:
                            topic_flag = True

                    if topic_flag:
                        train.append(random_sample)
                        continue

                raise ValueError(f"the configuration {(target, topic)} does not have enough rows to be split")
            else:
                n_train = max(1, min(random_sample.shape[0] - 1, round(random_sample.shape[0] * train_size)))
                train.append(random_sample.iloc[:n_train])
                test.append(random_sample.iloc[n_train:])

        train, test = pd.concat(train), pd.concat(test)

        if as_xy:
            train_y, test_y = train.pop(target_col), test.pop(target_col)
            return train, test, train_y, test_y, encoder
        else:
            return train, test, encoder

    def __repr__(self):
        return self.dataset.__repr__()
