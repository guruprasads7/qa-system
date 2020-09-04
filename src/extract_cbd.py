from SPARQLWrapper import SPARQLWrapper, N3, JSON
from rdflib import Graph
import pprint
from urllib.parse import urlencode, quote

sparql = SPARQLWrapper("http://dbpedia.org/sparql")


def fetch_resources_dbpedia(ontology_name, limit_count):
    query_string = ("\n"
                    "  PREFIX  dbo:  <http://dbpedia.org/ontology/>\n"
                    "  PREFIX  dbr:  <http://dbpedia.org/resource/>\n"
                    "\n"
                    "  SELECT DISTINCT ?s  \n"
                    "  WHERE\n"
                    "  { ?s  a    + dbo:" + ontology_name + ".\n"
                                                            "        \n"
                                                            "  } LIMIT " + limit_count + "\n"
                                                                                         "  ")
    sparql.setQuery(query_string)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    pprint.pprint(results, width=1)

    for result in results["results"]["bindings"]:
        print(result["s"]["value"])

    print('---------------------------')

    '''
    for result in results["results"]["bindings"]:
        print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))
    '''
    # for s in g:
    #  print((s.))
    # print(g.serialize(format='n3'))

    return results


def extract_cdb_of_resource(resources_dict):
    for result in resources_dict["results"]["bindings"]:
        uri_full_resource_name = result["s"]["value"]

        url_encode_resource_name = uri_full_resource_name.replace("'", "\u0027")

        resource_name = url_encode_resource_name.rsplit('/', 1)[-1].replace("'", "\\'")

        print("resource_name = ", resource_name)

        query_string = ("\n"
                        "    DEFINE sql:describe-mode \"CBD\"\n"
                        "  \n"
                        "    PREFIX foaf:  <http://xmlns.com/foaf/0.1/>\n"
                        "    PREFIX  dbo:  <http://dbpedia.org/ontology/>\n"
                        "    PREFIX  dbr:  <http://dbpedia.org/resource/>\n"
                        "  \n"
                        "    DESCRIBE "
                        + "dbr:" + resource_name + "\n"
                                                   "        \n"
                                                   "        ")

        sparql.setQuery(query_string)
        sparql.setReturnFormat(N3)
        results = sparql.query().convert()
        g = Graph()
        g.parse(data=results, format="n3")
        for s, p, o in g:
            print((s, p, o))
        # print(g.serialize(format='n3'))


def main():
    resources_dict = fetch_resources_dbpedia("Person", "10")

    extract_cdb_of_resource(resources_dict)
    # curl -X GET "https://api.dbpedia-spotlight.org/en/annotate?text=Who%20invented%20Skype" -H "accept: application/json"


if __name__ == "__main__":
    main()
