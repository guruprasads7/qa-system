import sys
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

#training_file_name = "data-files/sampledata.json"
training_file_name = "data-files/qald-9-train-multilingual.json"

def read_json_data(file_name):

    with open(file_name) as json_file:
        raw_json = json.load(json_file)

    raw_json_normailize_data_df = json_normalize(raw_json['questions'])

    raw_json_normailize_data_df = raw_json_normailize_data_df[raw_json_normailize_data_df['answertype'] != 'boolean']
    
    # Extract only the english questions from the json file using json_normalize
    question_data_df = json_normalize(raw_json_normailize_data_df.to_dict(orient="records"), record_path=['question'], meta=['id', 'answertype', 'aggregation', 'onlydbo','hybrid'])
    english_ques_df = question_data_df[question_data_df['language'] == 'en']

    ## Extract the Sparql questions from the json file
    sparql_query_df = raw_json_normailize_data_df[['id', 'query.sparql']]
  
    
    # Extract all the answers from the question above
    answers_data_df = json_normalize(raw_json_normailize_data_df.to_dict(orient="records"), record_path=['answers', 'results', 'bindings' ],meta=['id'], errors="skip" )

    #print(answers_data_df[['head.vars','results.bindings']])

    # Merging the query and questions dataframe on "id" column
    questions_query_df = pd.merge(english_ques_df,sparql_query_df, on='id')

    # Merge the question_query_df with answers dataframe again on the "id" column
    questions_query_answers_df = pd.merge(questions_query_df, answers_data_df, on='id')

    return(questions_query_df, questions_query_answers_df)

def read_answers_data(file_name):

    with open(file_name) as json_file:
        raw_json = json.load(json_file) 

    ## Extract the Sparql questions from the json file
    raw_json_normailize_data_df = json_normalize(raw_json['questions'])

    filter_boolean_results = raw_json_normailize_data_df[raw_json_normailize_data_df['answertype'] != 'boolean']

    answers_data_df = json_normalize(filter_boolean_results.to_dict(orient="records"), record_path=['answers','results', 'bindings' ],meta=['id'] )
    print(answers_data_df.count())

def extract_records_column_count(input_dataframe, unique_column_name, number_records_per_column):

    # Get the value counts based on a column name
    value_counts = input_dataframe[unique_column_name].value_counts()

    # Retrive number_records_per_column based on the  unique_column_name
    filtered_results_df = input_dataframe[input_dataframe[unique_column_name].isin(value_counts.index[value_counts.eq(number_records_per_column)])]

    return (filtered_results_df)

def main():
    #print("Starting the base code for IR mini project")
    questions_query_df, questions_query_answers_df = read_json_data(training_file_name)

    print("NUmber of results :",  questions_query_df.count())
    #read_answers_data(training_file_name)

    records_with_single_answer_df = extract_records_column_count(questions_query_answers_df, 'id', 1)

    print("Number of questions with only one answer : ", records_with_single_answer_df.count() )

if __name__ == "__main__":
    main()