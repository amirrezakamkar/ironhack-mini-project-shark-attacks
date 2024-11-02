# Shark Attacks

Our mission was to clean the messy dataset known as “Shark Attacks” that we get [from this link](https://www.sharkattackfile.net/incidentlog.htm) 

**Resources:**
- [Slides](https://github.com/markmorcos/ironhack-mini-project-shark-attacks/blob/main/Slides.pdf)
- [Cleaning functions](https://github.com/markmorcos/ironhack-mini-project-shark-attacks/blob/main/cleaning.py)
- [Date and Time](https://github.com/markmorcos/ironhack-mini-project-shark-attacks/blob/main/DateAndTime.ipynb)
- [Country and State (incl. Diagram)](https://github.com/markmorcos/ironhack-mini-project-shark-attacks/blob/main/CountryAndState.ipynb)

## Summary

Our project is about identifying the seasonal and location patterns of shark activity near Florida. 
By understanding when these encounters are most likely to occur, we can better:quip communities, local businesses, and tourists with the knowledge they need to enjoy Florida's beautiful beaches while coexisting safely with its marine wildlife.

## Dataset

The dataset was really messy and we applied the following changes:
  - Format dates with regex
  - Format time with regex
  - Format location (Country, State, Florida)

## Issues

- No pattern in injuries
- Multiple date/year formats
- No pattern in State
- Missing values
- Unnamed columns

## Solutions

- Data Wrangling and Cleaning
- We kept only the more relevant columns

## Non-profit Idea

Come up with information for local businesses and policy advice for local Floridian authorities and Florida.
- Find the 3 most “dangerous” hotspots to warn people

## Hypotheses

- In Florida, shark encounters can happen at any time of year, but they tend to spike in mid-spring as the waters warm up and more beachgoers head to the coast.
- Our project is about identifying the seasonal and location patterns of shark activity near Florida. 
By understanding when these encounters are most likely to occur, we can better equip communities, local businesses, and tourists with the knowledge they need to enjoy Florida's beautiful beaches while coexisting safely with its marine wildlife.

## Findings
Most of the attacks occur in the following locations:
- New Smyrna Beach, Volusia County.
- Daytona Beach, Volusia County.
- Ponce Inlet, Volusia County. 

## Conclusions

- Potential implications for raising awareness in the hotspot areas, especially during the peak time.
- Lack of data in developing countries.
