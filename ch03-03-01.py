from elasticsearch import Elasticsearch
es = Elasticsearch()

import pprint
pprint.pprint(es.info(pretty=True))
