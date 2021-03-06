'''
This script is meant to run StanfordCoreNLP parser and save the results for a whole data set.

This is a preparation step for feature extraction that takes a long time,
    so it is a good idea to separate this from the other steps.  
'''
import time

from contractions import fix
from pycorenlp.corenlp import StanfordCoreNLP

from nutrition.structure.data_set import DataSet
from nutrition.structure.counter import Counter
import sys
from nutrition.structure.environment import STANFORD_SERVER
from wnserver.stopwatch import Stopwatch


def process_stanford(data_set, restart=False):
    # load count, i.e. how many documents have been parsed successfully
    counter = Counter(data_set.stanford_path, restart=restart)
    
    # prepare to use Stanford parser
    nlp = StanfordCoreNLP(STANFORD_SERVER)

    start = time.time()
    while counter.count < data_set.data['count']:
        doc_start = time.time()
        
        # read file
        text = fix(data_set.get_text(counter.count))
        
        # call stanford annotate api
        annotation = nlp.annotate(text, properties={
            'annotators': 'lemma,parse',
            'outputFormat': 'json'
        })
        
        if type(annotation) is str:
            print('Error returned by stanford parser:', annotation)
            sys.exit()
        
        # pickle the result
        data_set.save_stanford_annotation(counter.count, annotation)
        
        # save the new count
        counter.increment()
        
        # print time information
        print('%i, %i%% %.2f seconds (%.0f total))' % (counter.count-1, 100*counter.count/data_set.data['count'], time.time() - doc_start, time.time() - start))


if __name__ == '__main__':
    process_stanford(DataSet('learning-corpus'), restart=False)

    # sw = Stopwatch()
    #
    # data_set = DataSet('cepp')
    # sw.lap('test')
    # nlp = StanfordCoreNLP(STANFORD_SERVER)
    # sw.lap('test')
    # text = fix(data_set.get_text(0))
    # print(text)
    # sw.lap('test')
    # annotation = nlp.annotate(text, properties={
    #     'annotators': 'lemma,parse',
    #     'outputFormat': 'json',
    #     'coref.algorithm': 'statistical'
    # })
    # sw.lap('test')
    # print(annotation)

    
    
    
    
    
    