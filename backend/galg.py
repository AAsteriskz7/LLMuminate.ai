import google.generativeai as genai
import ast

def tuplecreation(listOfTuples):
    returnList = []
    for string1, string2 in listOfTuples:
        genai.configure(api_key='YOUR KEY HERE')
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Analyze the two given strings, if the strings are similar in anyway and 
        they contain numbers that represent the same thing
        ONLY return the numbers in the format '(number1, number2)',
        OTHERWISE return 'no'

        String1: {string1}
        String2: {string2}
        """
        response = model.generate_content(prompt)
        if (response.text.strip() != "no"):
            return_tuple = ast.literal_eval(response.text.strip())
            returnList.append(return_tuple)
        else:
            returnList.append((string1, string2))
    print(returnList)
    return returnList

def compare_strings(string1, string2):
    genai.configure(api_key='AIzaSyCfe6L5MMhkgSC5Rc2KYxgWA-aXA74nhdQ')
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Analyze if the second string proves the first one incorrect.
    Respond with ONLY '0', '1' '2', 0 if nothing matches, 1 if it is partially correct, and 2 if its completely correct:

    String 1: {string1}
    String 2: {string2}"""
    
    response = model.generate_content(prompt)
    result = response.text.strip()
    # print(result)
    return int(result)

def calculate_percent_error(actual, expected):
    if expected == 0:
        expected = 0.000000001
    percent_error = 1.0 * (abs((actual - expected) / expected))
    return percent_error

def process_tuples(tuples_list):
    results = []
    for item in tuples_list:
        if isinstance(item[1], str):
            result = compare_strings(item[0], item[1])
            results.append(result)
        elif isinstance(item[1], (int, float)):
            result = calculate_percent_error(item[0], item[1])
            results.append(result)
    return results

def get_similarity_score(tuples_list) :
    created_tuple = tuplecreation(tuples_list)
    processed = process_tuples(created_tuple)
    sum = 0
    interval = 100 / len(processed)
    for info in processed:
        if type(info) == int:
            sum += int(interval * (info / 2.0))
        elif type(info) == float:
            sum += int(interval * (1 - info))
    return round(sum)

# tuples_list = [('carrots are healthy', 'carrots are healthy'), ('carrots are healthy', 'loads and loads and loads of chocolate is healthy'), ("wash your hands for 5 min", "wash your hands for 15 min")]
# print(get_similarity_score(tuples_list))
