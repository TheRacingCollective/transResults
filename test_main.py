from unittest import TestCase
from main import TransResultCalculator

class Test(TestCase):

    def setUp(self):
        self.calculator = TransResultCalculator(['wIrving'])

    def test_calc_results_startTimeOnly_riderAppearsInResults(self):
        timestamps = [{'handle': 'wIrving',
                       'start': '2021-05-28T20:00'}]
        expected_results = [{'Rider': 'wIrving',
                             'CP1': '',
                             'CP2': '',
                             'CP3': '',
                             'CP4': '',
                             'CP5': '',
                             'END': ''}]
        results = self.calculator.calc_results(timestamps)
        self.assertEqual(expected_results, results)

    def test_calc_results_startAndCp1_riderAppearsWithTime(self):
        timestamps = [{'handle': 'wIrving',
                       'start': '2021-05-28T20:00',
                       'cp1':   '2021-05-28T21:30'}]
        expected_results = [{'Rider': 'wIrving',
                             'CP1': '01H 30M',
                             'CP2': '',
                             'CP3': '',
                             'CP4': '',
                             'CP5': '',
                             'END': ''}]
        results = self.calculator.calc_results(timestamps)
        self.assertEqual(expected_results, results)

    def test_calc_results_startCp1AndCp2_riderAppearsWithCumulativeTime(self):
        timestamps = [{'handle': 'wIrving',
                       'start': '2021-05-28T20:00',
                       'cp1':   '2021-05-28T21:30',
                       'cp2':   '2021-05-28T22:45'}]
        expected_results = [{'Rider': 'wIrving',
                             'CP1': '01H 30M',
                             'CP2': '02H 45M',
                             'CP3': '',
                             'CP4': '',
                             'CP5': '',
                             'END': ''}]
        results = self.calculator.calc_results(timestamps)
        self.assertEqual(expected_results, results)

    def test_calc_results_missingTime_intermediateResultsAreBlanked(self):
        timestamps = [{'handle': 'wIrving',
                       'start': '2021-05-28T20:00',
                       'cp2':   '2021-05-28T21:30'}]
        expected_results = [{'Rider': 'wIrving',
                             'CP1': 'XXH XXM',
                             'CP2': '01H 30M',
                             'CP3': '',
                             'CP4': '',
                             'CP5': '',
                             'END': ''}]
        results = self.calculator.calc_results(timestamps)
        self.assertEqual(expected_results, results)

    def test_calc_results_riderNotSignedUp_notInResults(self):
        timestamps = [{'handle': 'iWashington',
                       'start': '2021-05-28T20:00',
                       'cp1':   '2021-05-28T21:30'}]
        expected_results = []
        results = self.calculator.calc_results(timestamps)
        self.assertEqual(expected_results, results)
