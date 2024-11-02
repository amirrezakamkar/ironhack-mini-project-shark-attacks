import pandas as pd
import matplotlib.pyplot as plt

# sharks_df = pd.read_excel('GSAF5.xls')
# sharks_df = sharks_df.drop(['pdf', 'Unnamed: 22', 'Unnamed: 21', 'Case Number.1', 'Case Number', 'href', 'href formula', 'Unnamed: 11'], axis=1)

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

def normalize_date(date):
    """
    Normalize date by changing it to lowercase and stripping unnecessary text

    Parameters:
    date: `str` or `datetime` object

    Returns:
    date: `str` or `datetime` object after normalizing it
    
    - `reported` was removed from the date column
    - `sept` is not an accepted `datetime` so it was replaced with `sep`
    - replace `nox` with `nov`
    """
    if isinstance(date, datetime): return date
    
    date = str(date).strip().lower()
    date = date.replace("reported", "")
    date = date.replace("september", "sep")
    date = date.replace("sept", "sep")
    date = date.replace("nox", "nov")
    
    return date

def match_date(regex, date):
    """
    - **Short dates:** 30-Oct-2024 or similar
    - **Long dates:** 30-October-2024 or similar
    - **Years**: 4 consecutive numbers
    
    ### Running regular expressions
    - If the date is already a Python `datetime` object, return the date as it is
    - First match long dates, short dates then years
    - Parse these dates into a Python `datetime` object
- If there are any errors, exclude that date

    Parameters:
    regex: `str`, regular expression
    date: `str`, date to be parsed

    Returns:
    `datetime` or None, formatted `datetime` object if possible
    """
    match = re.search(regex, date)
    if match:
        day = match.group(1).zfill(2)
        month = match.group(2)
        year = match.group(3)
        return datetime.strptime(f"{day}/{month}/{year}", "%d/%B/%Y")
    return None

def format_date(date):
    """
    Parameters:
    date: `str`, date to be parsed

    Returns:
    `datetime` or None, formatted `datetime` object if possible
    """
    if isinstance(date, datetime): return date

    short_date_regex = "([0-9]{1,2})[-\\s]+([a-zA-Z]{3,4})[-\\s]+([0-9]{4})"
    long_date_regex = "([0-9]{1,2})[-\\s]+([a-zA-Z]{4,10})[-\\s]+([0-9]{4})"

    try:
        long_date = match_date(long_date_regex, date)
        if long_date: return long_date

        short_date = match_date(short_date_regex, date)
        if short_date: return short_date

        return None
    except ValueError:
        return None

def normalize_year(year):
    """
    Parameters:
    date: `str`, year to be normalized

    Returns:
    `str`: formatted year or same input if not possible
    """
    if year >= 1000: return year
    if year >= 100: return float(f"1{year}")
    if year >= 25: return float(f"19{year}")
    if year >= 10: return float(f"20{year}")
    if year >= 0: return float(f"200{year}")
    return year

def infer_year(row):
    if pd.isnull(row.Year) and not pd.isnull(row.Date) and isinstance(row.Date, datetime):
        row.Year = row.Date.year
    return row

def month_grouping(date):
    if not isinstance(date, datetime): return date
    return date.strftime("%B")

def sanitize_time(time):
    """
    Parameters:
    time: `str`, time to be sanitized

    Returns:
    `str` or None, sanitized time if possible
    """
    long_time_regex = "([0-9]{1,2})[hr\\s\\.]*([0-9]{2})"
    short_time_regex = "([0-9]{1,2})[hr\\s\\.]*"

    if time in ["Not advised", "Not stated", "?"]: return None
    if not isinstance(time, str): time = str(time)
    
    try:
        long_time = re.search(long_time_regex, time)
        if long_time:
            hours = long_time.group(1).zfill(2)
            minutes = long_time.group(2)
            return f"{hours}:{minutes}"

        short_time = re.search(short_time_regex, time)
        if short_time:
            hours = short_time.group(1).zfill(2)
            return f"{hours}:00"

        return None
    except ValueError: return time