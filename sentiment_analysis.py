# ***************  Capstone Project  ***************
'''
This program uses the en_core_web_md spaCy model to analyse and classify a sample set 
of customer product review texts and makes sentiment predictions on them. 
Two most similar review texts with a reference base review text will also be output.

This program will:
- Read in the customer review dataset from the datafile
- Prepare and clean the dataset using the function clean_dataframe, and 
- Store the result in a variable named df_clean_reviews
- Store one-seventh of the size of the dataset in a variable called up_limit
- Ask the user to input the total number of review texts, within the range of ten 
    and up_limit, that need to be analysed and store the number in a variable called 
    called no_of_samples
- Generate a list of numbers from 0 to up_limit, representing the index of the dataset of 
    the results in a list variable called rows
- Generate a set of index numbers of the sample review texts, the size of the set is 
    specified by the variable no_of_samples
- Choose one other review text as the reference base review text in similarity comparisons
- Set up variables for storing data in sentiment analysis
- For each of the sampled review texts, do the following:
    - Perform the sentiment analysis on the sample review text by the function 
        sentiment_analysis, and
    - Store the returned results of the sentiment assessment of review text  in a 
        variables called res_sentiment
    - Add the review rating, review text, and the returned results in list variables
        called ratings, texts, text_sentiment respectively 
    - Add the polarity of the sentiment analysis to the list element of polarity specified 
        by the review rating
    - If review rating is greater than 3 and sentiment prediction is negative, or review 
        rating is less than 3 and sentiment prediction is positive, then
        - Extract one number from the head of the list rows and put it into a set variable 
            called special_texts
    - Otherwise, Extract one number from the head of the list rows and put it into a set 
        variable called general_texts
    - Check the similarity of the sampled review text against the reference base review text
    - If the similarity has a higher score than the other checks performed so far, then
        - If this is not the first review text, then
            - Copy highest_similarity, high_similar_text_no, high_similar_text_sentiment 
                to second_similarity, second_similar_text_no, second_similar_text_sentiment 
                respectively
        - Store the similarity score in a variable called highest_similarity
        - Store the index of the sampled review text in a variable called high_similar_text_no
        - Store the sentiment prediction of the sampled review text in a variable called 
            high_similar_text_sentiment
- Construct a data frame df_reviews_sentiment using the lists ratings, texts, and 
    text_sentiment with column labels 'Rating', 'Text', and 'Sentiment' respectively
- Count 3 times, in each count
    - If there is still index stored in special_texts,
        - Choose one index from special_texts, and
        - Print the sentiment analysis details of the chosen review text by calling the
            function print_one_row
    - If there is still index stored in general_texts,
        - Choose one index from those stored in general_texts,and
        - Print the sentiment analysis details of the chosen review text by calling the function 
            print_one_row 
- Perform the sentiment analysis on the reference review text by the function sentiment_analysis, and
- Store the returned results to a variable called ref_sentiment_results
- Print the results of similarity check and polarity of the sentiment analysis of the two
    review texts specified by indexes stored in high_similar_text_no and second_similar_text_no
- Prepare and show a violin graph of the spread of sentiment predictions grouped by each review rating
'''

# ------------------------------   START OF PROJECT CODE   ------------------------------

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
from random import randint
from matplotlib import pyplot as plt

nlp = spacy.load('en_core_web_md')   # the _md language model is used because similarity check will be performed
nlp.add_pipe("spacytextblob")
try:
    df_reviews = pd.read_csv('amazon_product_reviews.csv',sep=',')
except:
    print('File-reading Error: Please store the data file "amazon_product_reviews.csv" in the working directory.')
else:
    print(df_reviews.info())

    '''
    Function for DataFrame Preparation and Cleaning
        This function will
        - Prepare a copy of the dataset of the two columns 'reviews.rating' and 'review.text'
        - Put 0 into any reviews.rating cell with missing data
        - Change the data type of reviews.rating into integer type
        - Remove all entries with missing data
        - Remove all entries that are duplicates
        - Return the Re-indexed cleaned DataFrame
    '''
    def clean_dataframe(df):
        reviews_data = df[['reviews.rating','reviews.text']].copy()
        reviews_data['reviews.rating'].fillna(0, inplace = True)
        reviews_data['reviews.rating'] = pd.to_numeric(reviews_data['reviews.rating'],downcast='integer')
        reviews_data.dropna(inplace=True)
        reviews_data.drop_duplicates(inplace=True)
        return reviews_data.reset_index(drop=True)

    '''
    Function for Text Cleaning
        - Store a set of stop words to be excluded from the stop word list in a variable called not_stop
        - Store the stop words in the language model excluding those in not_stop in a variable 
            called my_stop_words 
        - Remove all stop words specified in my_stop_words from the text 
        - Remove all whitespaces from the text
        - Remove all punctuations from the text
        - Remove all proper nouns from the text
        - Change the whole string into lower case letters
        - Return the cleaned text
    '''
    def preprocess_text(text):
        not_stop ={'never','most','more','many','very','not','much','less','few','first','due','other',\
                    'no','really','least','top','above','down','full','last','only','enough','such','back',\
                    'only','several','next','mostly','own','whole','behind','becoming','former','third',\
                    'same','various','latterly','latter','serious','further', 'formerly', 'ten', 'empty'}
        my_stop_words = [item for item in spacy.lang.en.STOP_WORDS if not item in not_stop]
        for item in my_stop_words:
            text.replace(item, ' ')   # remove all stop words that would not affect sentiment analysis

        nlp_text = nlp(' '.join(text.split()))   # remove all whitespaces and apply the language model

        # remove all punctuations and proper nouns
        clean_tokens = [token.text for token in nlp_text if not (token.is_punct or token.pos_ == 'PROPN')]

        clean_text = " ".join(clean_tokens).lower()   # construct a clean text into one with lower case letters
        return clean_text
    
    '''
    Function for Sentiment Analysis
        This function will
        - Call the preprocess_text function to clean the review text
        - Apply the language analysis model to the cleaned text and Store the results in a variable 
            called nlp_review
        - Return the sentiment assessment results of the review text
    '''
    def sentiment_analysis(review_text):
        clean_review_text = preprocess_text(review_text)
        nlp_review = nlp(clean_review_text)
        return nlp_review._.blob.sentiment_assessments

    '''
    # Function to print the sentiment analysis results of one review text
        This function will
        - Print the review rating, review text and sentiment polarity of a review text
        - Group the positive tokens, neutral tokens and negative tokens along with their 
            respective polarities in variables called positive, neutral, negative respectively
        - Print positive, neutral and negative
    '''
    def print_one_row(df_results):
        print(f"\nReview rating: {df_results['Rating']}")
        print(f"Review text examined: \n{df_results['Text']}")
        print(f"Sentiment measures: \n   Polarity is {df_results['Sentiment'].polarity:.4f}")
        positive = [(item[0], item[1]) for item in df_results['Sentiment'].assessments if item[1] > 0]
        neutral = [(item[0], item[1]) for item in df_results['Sentiment'].assessments if item[1] == 0]
        negative = [(item[0], item[1]) for item in df_results['Sentiment'].assessments if item[1] < 0]
        if len(positive)+len(neutral)+len(negative) == 0:
            print(f'   No words related to sentiment found in the text.')
        else:    
            print(f"   Words used in the assessment of the full text:")
            if len(positive)>0: print(f"     positive words: {positive}")
            if len(neutral)>0: print(f"      neutral words: {neutral}")
            if len(negative)>0: print(f"     negative words: {negative}")


    # Prepare and clean the dataset, and show the infomation about the dataset
    df_clean_reviews = clean_dataframe(df_reviews)
    print(df_clean_reviews.info())

    # The index numbers of the review texts to be analysed are randomly generated, with
    # the total number entered by the user, which should be a number in the range of 10
    # and the one-seventh of the size of the dataset
    up_limit = df_clean_reviews.shape[0] // 7 
    while True:
        try:
            no_of_samples = int(input(f'Please input the number of samples (a number between 10 and {up_limit}): '))
        except:
            print(f'Input error: the input should be a number between 10 and {up_limit}.\n')
        else:
            if not no_of_samples in range(10,up_limit+1):
                print(f'Number error: the number should be between 10 and {up_limit}.\n')
            else:
                print('Processing ...')
                break
    rows = list(range(no_of_samples))
    sampled = set()
    while len(sampled) < no_of_samples:
        sampled.add(randint(0,df_clean_reviews.shape[0]-1))
    ref_text_no = randint(0,df_clean_reviews.shape[0]-1)   # one more text is sampled as a base text in similarity checking

    # The index of a review text as a reference text in the similarity comparison is chosen
    while ref_text_no in sampled:
        ref_text_no = randint(0,df_clean_reviews.shape[0]-1)

    # Initialisation of variables
    highest_similarity = -1.0
    ratings = list()
    texts = list()
    text_sentiment = list()
    polarities = [[0],[0],[0],[0],[0],[0]]
    general_texts = set()
    special_texts = set()

    # Apply language analysis model to the dataset
    for item in sampled:
        res_sentiment = sentiment_analysis(df_clean_reviews['reviews.text'][item])

    # Data about the analysis are added to respective lists for construction of DataFrame later
        ratings.append(df_clean_reviews['reviews.rating'][item])
        texts.append(df_clean_reviews['reviews.text'][item])
        text_sentiment.append(res_sentiment)
        polarities[df_clean_reviews['reviews.rating'][item]].append(res_sentiment.polarity)
        if (df_clean_reviews['reviews.rating'][item]>3 and res_sentiment.polarity<0) or \
            (df_clean_reviews['reviews.rating'][item]>0 and df_clean_reviews['reviews.rating'][item]<3 \
            and res_sentiment.polarity>0): 
            special_texts.add(rows.pop(0))
        else:
            general_texts.add(rows.pop(0))

    # Similarity check with the reference review text
        similarity = nlp(preprocess_text(df_clean_reviews['reviews.text'][ref_text_no])).similarity\
                        (nlp(preprocess_text(df_clean_reviews['reviews.text'][item])))
        if similarity > highest_similarity:
            if highest_similarity > -1:
                second_similarity = highest_similarity
                second_similar_text_no = high_similar_text_no
                second_similar_text_sentiment = high_similar_text_sentiment
            highest_similarity = similarity
            high_similar_text_no = item
            high_similar_text_sentiment = res_sentiment

    # A dataframe of the sentiment analysis results is formed
    df_reviews_sentiment = pd.DataFrame({'Rating':ratings,'Text':texts,'Sentiment':text_sentiment})

    # Print the sentiment analysis results of at most 6 selected review texts
    for counting in range(3):
        if len(special_texts)>0:
            row = special_texts.pop()
            print_one_row(df_reviews_sentiment.iloc[row])
        if len(general_texts)>0:
            row = general_texts.pop()
            print_one_row(df_reviews_sentiment.iloc[row])

    # Print the sentiment analysis results and similarity measures of review texts
    ref_sentiment_results = sentiment_analysis(df_clean_reviews['reviews.text'][ref_text_no])
    print(f'\nThe following two review texts are having a similar score of {highest_similarity}')
    print(f'\nReview Text 1 (sentiment polarity = {ref_sentiment_results.polarity}) :')
    print(df_clean_reviews['reviews.text'][ref_text_no],'\n')
    print(f'Review Text 2 (sentiment polarity = {high_similar_text_sentiment.polarity}) :')
    print(df_clean_reviews['reviews.text'][high_similar_text_no],'\n')
    print(f'\nThe following review two texts are having a similar score of {second_similarity}')
    print(f'\nReview Text 1 (sentiment polarity = {ref_sentiment_results.polarity}) :')
    print(df_clean_reviews['reviews.text'][ref_text_no],'\n')
    print(f'Review Text 2 (sentiment polarity = {second_similar_text_sentiment.polarity}) :')
    print(df_clean_reviews['reviews.text'][second_similar_text_no],'\n')

    # Show a violin plot graph on the spread of the sentiment polarity measures grouped by review ratings
    plt.violinplot(polarities,positions=[0,1,2,3,4,5],widths=0.3)
    plt.xlabel('Review rating')
    plt.ylabel('Review text sentiment polarity')
    plt.title('Amazon Customer Review Text Sentiment Study')
    plt.show()


# -------------------------------   END OF PROJECT CODE   -------------------------------
