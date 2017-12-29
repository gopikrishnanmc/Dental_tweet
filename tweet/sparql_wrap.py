from SPARQLWrapper import SPARQLWrapper, JSON


wikidata_endpoint = "https://query.wikidata.org/sparql"

dentists_query = """
SELECT DISTINCT ?Dentists ?DentistsLabel ?DateOfBirth ?sitelink ?image ?CitizenCountryLabel ?SexGenderLabel 
WHERE{
?Dentists ?o wd:Q27349.
?Dentists wdt:P569 ?DateOfBirth.
?Dentists wdt:P21 ?SexGender.
OPTIONAL{
  ?Dentists wdt:P18 ?image. 
  ?Dentists wdt:P27 ?CitizenCountry.
}
{?sitelink schema:about ?Dentists . 
?sitelink schema:inLanguage "en".
}
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

FILTER (SUBSTR(str(?sitelink), 1, 25) = "https://en.wikipedia.org/").
FILTER ( ?DateOfBirth>= "1600-01-01T00:00:00Z"^^xsd:dateTime).
BIND (COALESCE(?image,"unknown") AS ?image).
BIND (COALESCE(?CitizenCountryLabel,"unknown") AS ?CitizenCountryLabel).
}
ORDER BY ?Dentists
LIMIT 1000
"""

career_query = """
SELECT DISTINCT ?Dentists ?DentistsLabel ?DateOfBirth ?OccupationLabel ?sitelink 
WHERE {
  ?Dentists wdt:P106 wd:Q27349;
            wdt:P106 ?Occupation;
            wdt:P31 wd:Q5;
            wdt:P569 ?DateOfBirth;
            rdfs:label ?DentistsLabel.
  ?Occupation rdfs:label ?OccupationLabel.
  {?sitelink schema:about ?Dentists .
  ?sitelink schema:inLanguage "en".}
  FILTER (SUBSTR(str(?sitelink), 1, 25) = "https://en.wikipedia.org/")
  FILTER (?Occupation != wd:Q27349)
  FILTER (lang(?DentistsLabel) = "en")
  FILTER (lang(?OccupationLabel) = "en")
}
ORDER BY ?DentistsLabel
"""

class SPARQLQuery:
    """
    This class queries a SPARQL endpoint and returns a JSON representation of the data
    """

    def __init__(self, endpoint, query):
        self.endpoint = endpoint
        self.query = query

    def results(self):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(self.query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    def print_results(self, data_text):
        results = self.results()
        print(results)
        for result in results["results"]["bindings"]:
            print(result[data_text]['value'])


wiki_dent = SPARQLQuery(wikidata_endpoint, dentists_query)

dental_career = SPARQLQuery(wikidata_endpoint, career_query)
