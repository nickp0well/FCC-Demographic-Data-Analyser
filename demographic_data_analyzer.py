import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()
    
    # What is the average age of men?
    age_averages_per_sex = df[["age", "sex"]].groupby("sex").mean()
    average_age_men = round(age_averages_per_sex.loc['Male'].item(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    education_counts = df[["age", "education"]].groupby("education").count()
    value = (education_counts.loc['Bachelors'].item() / len(df)) * 100
    percentage_bachelors = round(value, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    df_salaryover50k = df[df["salary"] == '>50K']
    df_refined = df_salaryover50k[["education", "salary"]].groupby("education").count()
    total_higher_ed_over50k = df_refined.loc['Bachelors'].item() + df_refined.loc['Masters'].item() + df_refined.loc['Doctorate'].item()
    total_higher_ed = education_counts.loc['Bachelors'].item() + education_counts.loc['Masters'].item() + education_counts.loc['Doctorate'].item()
    value = (total_higher_ed_over50k / total_higher_ed) * 100
    higher_education_rich = round(value, 1)
    # What percentage of people without advanced education make more than 50K?
    df_refined_lowered = df_refined.drop(['Bachelors', 'Doctorate', 'Masters'])
    total_lower_ed_over50k = df_refined_lowered['salary'].sum()
    total_lower_ed_df = education_counts.drop(['Bachelors', 'Doctorate', 'Masters'])
    total_lower_ed = total_lower_ed_df['age'].sum()
    value = (total_lower_ed_over50k / total_lower_ed) * 100 
    lower_education_rich = round(value, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    df_minhours= df[df["hours-per-week"] == 1]
    num_minhours = len(df_minhours)
    df_minhours_over50k = df_minhours[df_minhours["salary"] == '>50K']
    num_minhoursover50k = len(df_minhours_over50k)
    value = (num_minhoursover50k / num_minhours) * 100
    rich_percentage = round(value, 1)

    # What country has the highest percentage of people that earn >50K?
    over50k = df[df["salary"] == '>50K']
    over50k_country = over50k[["native-country", "salary"]].groupby("native-country").count()
    df_countrycount = df[["native-country", "age"]].groupby("native-country").count()
    merged_tables = pd.merge(over50k_country, df_countrycount, how = "inner", on = "native-country")
    merged_tables["Proportion"] = merged_tables["salary"] / merged_tables["age"]
    percentage = merged_tables['Proportion'].max()
    country_name = merged_tables.index[merged_tables['Proportion'] == percentage].item()
    highest_earning_country = country_name
    highest_earning_country_percentage = round((percentage * 100), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    over50k = df[df["salary"] == '>50K']
    over50kindia = over50k[over50k["native-country"] == 'India']
    over50kindiagrouped = over50kindia[["occupation", "salary"]].groupby("occupation").count()
    value = over50kindiagrouped['salary'].max()
    valuename = over50kindiagrouped.index[over50kindiagrouped['salary'] == value].item()
    top_IN_occupation = valuename

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
