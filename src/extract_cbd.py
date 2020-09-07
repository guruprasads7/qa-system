from collections import defaultdict

from SPARQLWrapper import SPARQLWrapper, N3, JSON
from rdflib import Graph
import pprint

from typing import List
from urllib.parse import urlencode, quote
import json

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


def fetch_all_organizations(ontology_name, limit_count):
    # This would get you the first 10000 results. To get the next 10000, just add 10000 to the offset: LIMIT 10000 OFFSET 10000. Then, the next 10000 with OFFSET 20000, and so on.
    organizations_query = ("\n"
                           "      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
                           "    PREFIX dbo: <http://dbpedia.org/ontology/>\n"
                           "    SELECT ?org {\n"
                           "      SELECT DISTINCT ?org {\n"
                           "        ?org a/rdfs:subClassOf* dbo:Organisation .\n"
                           "     } ORDER BY ?org\n"
                           "    }\n"
                           "    LIMIT 10000 OFFSET 0\n"
                           "      ")

    sparql.setQuery(organizations_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    pprint.pprint(results, width=1)

    for result in results["results"]["bindings"]:
        print(result["org"]["value"])

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

        resource_string_explicit = "http://dbpedia.org/resource/Skype"

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
                        + "<" + resource_string_explicit + ">" + "\n"
                                                                 "        \n"
                                                                 "        ")

        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        filtered_english_results = get_only_english_results(results)

        print("Only Filtered English Json results = ", filtered_english_results)

        transformed_results = transform_and_group_cbd_results(filtered_english_results)

        print("Transformed results = ", transformed_results)


def get_only_english_results(json_string):

    output_json_string_array = []
    for result in json_string["results"]["bindings"]:
        # Extracting only english results for processing
        if "lang" in result["o"]:
            if result['o']['lang'] == "en":
                output_json_string_array.append(result)
        else:
            output_json_string_array.append(result)

    return output_json_string_array;


def transform_and_group_cbd_results(filtered_english_results):

    transformed_results = defaultdict()
    key = filtered_english_results[0].get('s')
    values_list = []

    list_dict = []
    for result_dict in filtered_english_results:
        stripped_dict = {}
        new_list = [{key: result_dict[key] for key in result_dict.keys() & {'p', 'o'}}]  # type: List[dict]
        stripped_dict['object'] = result_dict.get('o')
        stripped_dict['predicate'] = result_dict.get('p')

        list_dict.append(stripped_dict)
        values_list.append(new_list)

    # Extract the common subject from the results and adding the predicate object pairs
    transformed_results['subject'] = key
    transformed_results['predicate_object'] = list_dict

    return transformed_results


def main():
    # fetch_all_organizations("Person", "100")
    resources_dict = fetch_resources_dbpedia("Person", "1")

    extract_cdb_of_resource(resources_dict)
    # curl -X GET "https://api.dbpedia-spotlight.org/en/annotate?text=Who%20invented%20Skype" -H "accept: application/json"


if __name__ == "__main__":
    main()
