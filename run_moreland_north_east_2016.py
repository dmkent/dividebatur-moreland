"""Script to run the moreland count."""
from os.path import join, isfile, basename, isdir
from os import makedirs
import yaml

from dividebatur import counter
from dividebatur import results

from load_votes import load_votes


VEC_DATA = 'https://www.vec.vic.gov.au/results/general/MorelandNorth-EastWard2016ResultsByVotingCentre.xls'

def run(data_dir='moreland_north_east_2016_data'):

    candidates = yaml.load(open(join(data_dir,
                                     'candidates.yaml')))
    candidate_ids = range(len(candidates))
    def ident_for_candidate(name):
        return candidates.index(name)

    data_file = basename(VEC_DATA)
    data_on_disk = join(data_dir, data_file)
    if not isfile(data_on_disk):
        data_to_load = VEC_DATA
    else:
        data_to_load = data_on_disk

    print(data_to_load)
    data = load_votes(data_to_load)
    data.columns = [s.split(',')[0].lower() for s in data.columns]
    first_prefs = data.ix['TOTAL ALL VOTE TYPES'].ix[:20]
    print(first_prefs)

    htvs = yaml.load(open(join(data_dir, 'how_to_vote_cards.yaml')))

    htvs = {k.lower(): tuple(map(lambda s: s.lower(), htvs[k])) for k in htvs}
    def assume_htv(for_cand, from_cand):
        prefs = list(htvs[from_cand])
        del prefs[prefs.index(for_cand)]
        prefs.insert(0, for_cand)
        return tuple(prefs)

    ##
    # No how-to-vote info for hong or gartside
    # Assume similar to irfanli
    htvs['hong'] = assume_htv('hong', 'irfanli')
    htvs['gartside'] = assume_htv('gartside', 'irfanli')

    # Greens have single HTV. Reuse for candidate 2 and 3
    htvs['pulford'] = assume_htv('pulford', 'abboud')
    htvs['mcgilvray'] = assume_htv('mcgilvray', 'abboud')

    htvs_ids = {name: tuple(ident_for_candidate(c) for c in htvs[name]) for name in htvs.keys()}

    if not isdir('logs'):
        makedirs('logs')
    ne_results = results.JSONResults(
        'angular/data/ne.json',
        'logs',
        candidate_ids,
        candidate_ids,
        lambda a: a,
        lambda a: candidates[a],
        lambda a: candidates[a],
    )

    tickets = counter.PapersForCount()
    for candidate in first_prefs.index:
        tickets.add_ticket(htvs_ids[candidate], first_prefs[candidate])

    c = counter.SenateCounter(
        ne_results,
        4,
        tickets,
        lambda e: 0,
        lambda e: 0,
        lambda e: 0,
        candidate_ids,
        lambda a: a,
        True,
    )
    c.run()

if __name__ == '__main__':
    run()
