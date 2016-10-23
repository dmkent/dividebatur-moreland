"""Load data from VEC."""
import pandas

def load_votes(fname):
    """Load excel from from VEC.

       e.g. https://www.vec.vic.gov.au/results/general/MorelandNorth-EastWard2016ResultsByVotingCentre.xls
    """
    data = pandas.read_excel(fname)
    votes = data.iloc[13:, 2:]
    votes.index = data.iloc[13:, 1]
    votes.columns = data.iloc[11, 2:].str.strip().str.replace('\n', ' ')
    votes = votes.dropna(how='all', axis=0).dropna(how='all', axis=1)
    return votes

if __name__ == '__main__':
    data = load_votes('MorelandNorth-EastWard2016ResultsByVotingCentre.xls')
