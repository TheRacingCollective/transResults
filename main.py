import json
import boto3
from datetime import datetime


class TransResultCalculator(object):

    def __init__(self, signups):
        self.signups = [s.lower() for s in signups]

    def calc_results(self, timestamps):
        data = []
        no_signup = []
        no_start = []
        started = []
        for r in timestamps:
            handle = r['handle']
            started.append(handle.lower())
            if handle.lower() not in self.signups:
                no_signup.append(handle)
                continue
            d = {'Rider': handle, 'CP1': '', 'CP2': '', 'CP3': '', 'CP4': '', 'CP5': '', 'END': ''}
            if 'start' not in r:
                no_start.append(handle)
                continue
            st = datetime.strptime(r['start'], '%Y-%m-%dT%H:%M')
            for cp in ['cp1', 'cp2', 'cp3', 'cp4', 'cp5', 'end']:
                if cp in r:
                    cpt = datetime.strptime(r[cp], '%Y-%m-%dT%H:%M')
                    d[cp.upper()] = self.format_time(cpt - st)
            passed = False
            for cp in ['end', 'cp5', 'cp4', 'cp3', 'cp2', 'cp1']:
                if d[cp.upper()]:
                    passed = True
                if passed and not d[cp.upper()]:
                    d[cp.upper()] = 'XXH XXM'
            data.append(d)
        print('%s rider(s) posted, %s percent of signups.' % (len(data), len(data) * 100 // len(self.signups)))
        if no_signup:
            print('%s rider(s) did not signup - %s.' % (len(no_signup), ', '.join(no_signup)))
        if no_start:
            print('%s rider(s) have no start time - %s.' % (len(no_start), ', '.join(no_start)))
        not_started = [s for s in self.signups if s not in started]
        if not_started:
            print('Not started: ' + ', '.join(not_started))
        return data

    @staticmethod
    def format_time(td):
        hours = (td.seconds // 3600)
        minutes = (td.seconds % 3600) // 60
        return '{:02g}H {:02g}M'.format(hours, minutes)


terSignups = ['willschrimshaw', 's2martin', 'carl_hopps', 'charlesabeasley', 'radhartgeorge', 'dr_stav', 'si_hunter1',
              'richyjmo', 'ihhudson01', 'masondurant', 'nerohadsi', 'dulcepedroso1', 'jimarmshaw', 'jsallan918',
              'dubert01', 'markcjagar', 'dave_blogs', 'verangosi', 'pedurr1', 'miscsheep', 'milesresso', '_timwalton_',
              'paulwilliamslab', 'rob_webb_dbbc', 'lynd_nick', 'leeboybrown', 'hlarbalestier', 'sam88thompson',
              'nicholasbarna19', 'cimermannicolas', 'chris_c_wilcox', 'lizziej61392895', 'baston_john', 'im_ed_m',
              'nickyshaw12', 'timwelsh_', 'gfromabove', 'rideoffline', 'p_boynton', 'nicktatt', 'chasingpeloton',
              'rms2382', 'beth_jacks12', 'rhodsprice', 'jamieol06455602', 'clarewalkeden', 'liambromiley',
              'gutsibikes']


def run_update(upload=False):
    with open('timestamps.json') as f:
        results = json.loads(f.read())
    calculator = TransResultCalculator(terSignups)
    results = calculator.calc_results(results)
    if upload:
        s3 = boto3.resource('s3')
        path = 'racingCollective/trans/england/21.json'
        upload_results(s3, path, results)


def upload_results(s3, path, results):
    body = json.dumps({'data': results})
    s3.Object('bikerid.es', path).put(Body=body, ContentType='application/json')


if __name__ == '__main__':
    run_update(True)
