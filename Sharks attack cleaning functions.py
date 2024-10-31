import pandas as pd
import matplotlib.pyplot as plt

sharks_df = pd.read_excel('https://www.sharkattackfile.net/spreadsheets/GSAF5.xls')
sharks_df = sharks_df.drop(['pdf', 'Unnamed: 22', 'Unnamed: 21', 'Case Number.1', 'Case Number', 'href', 'href formula', 'Unnamed: 11'], axis=1)

def country_clean(sharks_df):
    """
    Cleans and standardizes the 'Country' column in the provided DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing a 'Country' column.

    Returns:
    pd.DataFrame: The DataFrame with a cleaned 'Country' column.
    """
    #removing the NA values
    sharks_df = sharks_df.dropna(subset=['Country'])

    sharks_df['Country'] = sharks_df['Country'].str.split(' / ')
    sharks_df = sharks_df.explode('Country')

    #replace bad entries with a single country but too repetitive doesn't show true data cleaning
    sharks_df['Country'] = sharks_df['Country'].replace({'CEYLON (SRI LANKA)': 'Sri Lanka'})
    sharks_df['Country'] = sharks_df['Country'].replace({'ST HELENA, British overseas territory': 'Saint Helena'})

    #lowercased the countries
    sharks_df["Country"] = sharks_df["Country"].str.lower()
    
    #Call method strip to strip off question marks at the end
    sharks_df['Country'] = sharks_df['Country'].str.strip('?')

    # For case-insensitive match
    sharks_df = sharks_df[~sharks_df['Country'].str.contains('asia|africa|ocean|sea|gulf', case=False, regex=True, na=False)]
    return sharks_df

def get_cleaned_usa_shark_data(sharks_df):
    """
    Filters and cleans shark attack data specific to the USA, focusing on state names.
    
    Parameters:
    shadf(pd.DataFrame): The input DataFrame containing 'Country' and 'State' columns.
    
    Returns:
    pd.DataFrame: A cleaned DataFrame with USA shark attack data and standardized state names.
    """
    
    # Filter data to include only USA entries
    sharks_usa = sharks_df.groupby("Country").get_group("usa")

    # Convert state names to lowercase
    sharks_usa["State"] = sharks_usa["State"].str.lower()

    # Correct specific misspelled or erroneous entries
    sharks_usa['State'] = sharks_usa['State'].replace({
        'noirth carolina': 'north carolina'
    })

    # Remove entries with specific incorrect data
    sharks_usa = sharks_usa[sharks_usa["State"] != 'cuba']

    return sharks_usa
