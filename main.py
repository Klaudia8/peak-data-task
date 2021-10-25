import pandas as pd
from numpy import nan
from ast import literal_eval
import os


# read data from csv file
def read_data(file):
    df = pd.read_csv(file, index_col='temp_id', usecols=['temp_id', 'authors'])
    df = df.loc[~df['authors'].isna()]  # eliminate rows with NA values

    print('data read.')
    return pd.DataFrame(df)


# extract authors from column with many authors in one row
def extract_authors(df, col):
    df = df[col].apply(literal_eval).explode(',')
    df = df.str.lower().drop_duplicates()  # drop duplicates, ignoring capital letters

    print('extract_authors processed.')
    return df


def split_column_to_multiple_columns(df):
    df = df.apply(lambda x: pd.Series(x.split(' ')))
    print('split_column_to_multiple_columns processed.')
    return df


def extract_surname_with_parts(df):
    parts = ['del', 'den', 'der', 'de', 'el', 'la', 'los', 'van', 'von']  # list of surnames' prefixes
    which_words = df.isin(parts)  # find surnames' prefixes in dataframe

    part_expression_idxs = []
    # create list with indexes and columns for expressions with surnames' prefixes
    for row in which_words.index:
        for col in which_words.columns:
            if which_words.loc[row, col]:
                part_expression_idxs.append([row, col])

    # insert True after surnames' prefixes
    for expr in part_expression_idxs:
        which_words.loc[expr[0], expr[1]:] = True

    # extract surnames with different prefixes
    surname_parts = df[which_words]
    which_na = df[which_words].isna().all(axis=1)
    surname_parts = surname_parts[~which_na]

    surnames = surname_parts[surname_parts.columns[1:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    print('extract_surname_with_parts processed.')
    return surnames


# extract last word (one-word surname) from authors
def extract_last_word(df):
    df = df.apply(lambda x: pd.Series([x.split(' ')[-1]]))
    print('extract_last_word processed.')
    return df


# merge one-word surname with surnames' parts
def combine_surnames(df, df1, df2):
    df1 = pd.merge(df1, pd.DataFrame(df2), left_index=True, right_index=True, how='left')
    df['surname'] = df1.apply(lambda x: x['0_x'] if x['0_y'] is nan else x['0_y'], axis=1)

    print('combine_surnames processed.')
    return df


# create dataframe separately with name and surname
def extract_full_names(df, col):
    df['name'] = df.apply(lambda x: x[col].replace(x['surname'], ''), axis=1).str.strip()
    df = df[['name', 'surname']]
    df = df.sort_values(by='surname')

    print('extract_full_names processed.')
    return df


# remove duplicated values based on first letter of the name
def remove_duplicates(df):
    df = df.assign(length=df['name'].apply(lambda x: len(x)))
    df = df.assign(first_letter=df['name'].str[0])
    df = df.sort_values(by=['surname', 'length', 'first_letter'], ascending=[True, False, True])
    duplicated = df[df[['surname', 'first_letter']].duplicated()]
    duplicated = duplicated.loc[duplicated['length'] == 1]
    df = df.loc[~df.index.isin(duplicated.index)]
    return df[['name', 'surname']]


if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), 'data/publications_min.csv')
    print(file_path)
    data = read_data(file_path)
    data = extract_authors(data, 'authors')
    data_full_name = pd.DataFrame(data.copy(deep=True))

    last_word = extract_last_word(data)
    data = split_column_to_multiple_columns(data)
    surname_part = extract_surname_with_parts(data)

    data = combine_surnames(data_full_name, last_word, surname_part)
    data = extract_full_names(data, 'authors')

    data = remove_duplicates(data)
    data.to_csv('unique_people.csv', index=False)
    print('data saved.')
