FROM docker.elastic.co/elasticsearch/elasticsearch:7.5.2@sha256:771240a8e1c76cc6ac6aa740d2b82de94d4b8b7dbcca5ad0cf49d12b88a3b8e7
RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
