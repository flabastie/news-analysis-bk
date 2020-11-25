import pprint
import re
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk import FreqDist
import json
from nltk.stem.snowball import FrenchStemmer
from elasticsearch import Elasticsearch
from datetime import datetime

class TransformationData():

    '''Data transformationData : Tokenizer and stopwords'''
    es = None
    index_name = None
    
    def __init__(self, index_name):

        '''
            Create an Elasticsearch connection object
            :param index_name: index name
            :type index_name: string
            :return: null
        '''

        self.es = Elasticsearch(
            ['https://00e8f2e302a74e0eafaa5aceffe44491.francecentral.azure.elastic-cloud.com:9243'],
            http_auth=('elastic', 'OhRgseujhwTV7WZye1S6qNio'),
            scheme="https", 
            port=443,)
        self.index_name = index_name

    def liste_auteurs(self):

        '''
            Get auteurs list
            :param self: self
            :type self: None
            :return: liste_auteurs
            :rtype: list
        '''

        res = self.es.search(index=self.index_name, body={
                "size": 0,
                "aggs": {
                    "auteurs": {
                    "terms": { "field": "author.keyword", "size": 10000 } 
                    }
                }
            }
        )
        auteurs_doc_list = res['aggregations']
        liste_auteurs = [ item['key'] for item in auteurs_doc_list['auteurs']['buckets'] ]
        return liste_auteurs
        
    def liste_sections(self):

        '''
            Get sections list
            :param self: self
            :type self: None
            :return: liste_sections
            :rtype: list
        '''

        res = self.es.search(index=self.index_name, body={
                "size": 0,
                "aggs": {
                    "sections": {
                    "terms": { "field": "section.keyword", "size": 10000 } 
                    }
                }
            }
        )
        sections_doc_list = res['aggregations']
        liste_sections = [ item['key'] for item in sections_doc_list['sections']['buckets'] ]
        return liste_sections

    def liste_types(self):

        '''
            Get types list
            :param self: self
            :type self: None
            :return: liste_types
            :rtype: list
        '''

        res = self.es.search(index=self.index_name, body={
                "aggs": {
                    "types": {
                    "terms": { "field": "type.keyword", "size": 10000 } 
                    }
                }
            }
        )
        types_doc_list = res['aggregations']
        liste_types = [ item['key'] for item in types_doc_list['types']['buckets'] ]
        return liste_types

# -------------------------
# main
# -------------------------

# instanciation
#transformData = TransformationData('news_analysis')
transformData = TransformationData('2months_covid')

#auteurs_list = transformData.liste_auteurs()
#pprint.pprint(auteurs_list)

#sections_list = transformData.liste_sections()
#pprint.pprint(sections_list)

types_list = transformData.liste_types()
pprint.pprint(types_list)
    