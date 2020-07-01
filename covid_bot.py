
# Smart Chat bot program

# importing library
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import string
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

warnings.filterwarnings("ignore")

import pandas as pd

pd.set_option('max_colwidth', 100)  # Increase column width
data = pd.read_excel(r"C:\Users\USER\Downloads\covid_bot\covid.xlsx", encoding='utf8')
# data.head(13)

data = np.array(data)

context = data[:, 0]
answers = data[:, 1]


# greetings
def greeting_response(text):
    text = text.lower()
    bot_greetings = ['hello', 'bonjour', 'hola', 'hey', 'hi']
    user_greetings = ['hello', 'bonjour', 'hola', 'hey', 'greetings', 'hi',"hii there", "hi there", "I am glad! You are talking to me"]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index


def bot_response(user_input):
    user_input = user_input.lower()
    context1 = list(context)
    context1.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(context1)
    similarity_score = cosine_similarity(cm[-1], cm)  # compares user last question to rest of the count matrix
    similarity_score_list = similarity_score.flatten()  # dimentionality reduction
    index = index_sort(similarity_score_list)  # arrange the indices in descending order of similarity score
    index = index[1:]  # all the indices leaving the sentence itself(entered by the user)
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_score_list[index[i]] > 0.0:
            bot_response += " " + data[index[i], 1]  # most similar sentence
            response_flag = 1
            j += 1  # no. of scores > 0

            if j >= 4:
                break  # to limit the no. of responses
        if response_flag == 0:
            bot_response += " " + "I appologize..... I don't understand"
        context1.remove(user_input)
        return bot_response




# read data
latest_state = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
latest_state1 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')

# save as a .csv file`
latest_state.to_csv('state_level_latest.csv', index=False)
latest_state1.to_csv('state_level_latest.csv', index=False)

# few rows
# latest_state.head(38)

# read data
district_wise = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
district_wise1 = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
# save as .csv file
district_wise.to_csv('district_level_latest.csv', index=False)
district_wise1.to_csv('district_level_latest.csv', index=False)

# first few rows
# district_wise.head(798)

latest_state = np.array(latest_state)
district_wise = np.array(district_wise)
state = latest_state[:, 0]
district = district_wise[:, 4]

# state cases output
dist1 = []


def state_cases(user_input):
    user_input = user_input.lower()
    user = user_input.split()[1]
    state1 = list(state)
    state1.append(user)
    response = ""
    cm2 = CountVectorizer().fit_transform(state1)
    similarity_score = cosine_similarity(cm2[-1], cm2)  # compares user last question to rest of the count matrix
    similarity_score_list = similarity_score.flatten()  # dimentionality reduction
    index = np.argmax(similarity_score_list[:len(similarity_score_list) - 1])
    # print(index)
    response_flag = 0
    similarity_score_list.sort()
    similarity_score_list = similarity_score_list[::-1]
    # print(similarity_score_list)
    # print(index)
    if similarity_score_list[0] > 0.0:
        response_flag = 1
    if response_flag == 0:
        response += " " + "I appologize..... I don't understand"
        return response
        state1.remove(user)
    return (latest_state1.iloc[index, 0:6])


# district cases output
dist1 = []


def district_cases(user_input):
    user_input = user_input.lower()
    user = user_input.split()[1]
    dist1 = list(district)
    dist1.append(user)
    response = ""
    cm1 = CountVectorizer().fit_transform(dist1)
    similarity_score = cosine_similarity(cm1[-1], cm1)  # compares user last question to rest of the count matrix
    similarity_score_list = similarity_score.flatten()  # dimentionality reduction
    index = np.argmax(similarity_score_list)
    # print(index)
    response_flag = 0
    similarity_score_list.sort()
    similarity_score_list = similarity_score_list[::-1]
    if similarity_score_list[0] > 0.0:
        # response+=" "+ district_wise1.iloc[index,5:8]#most similar sentence
        response_flag = 1
    if response_flag == 0:
        response += " " + "I appologize..... I don't understand"
        return response
    dist1.remove(user)
    return (district_wise1.iloc[index, 4:8])


# start the chat
def chat(user_input):

    exit_list = ["exit", 'see you later', 'quit', 'end', 'bye']
    while True:
        user_input = user_input.lower()
        if user_input in exit_list:
            return ("Doc Bot: Sgining Out...........")
            break
        else:
            if greeting_response(user_input) != None:
                return (greeting_response(user_input))
            elif (user_input.split()[0] == "district"):
                return (district_cases(user_input))
            elif (user_input.split()[0] == "state"):
                return (state_cases(user_input))
            else:
                return (bot_response(user_input))