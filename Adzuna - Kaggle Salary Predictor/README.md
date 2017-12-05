## Summary

This is a quick and dirty natural language processing notebook exploring the Adzuna Job Salary Prediction dataset from Kaggle. To access this dataset, you must download it from kaggle directly at https://www.kaggle.com/c/job-salary-prediction/data. 

This data was made available by Adzuna, a London headquartered job website, so they could better predict the appropriate salary given mostly unstructured, text based features, like: Job title, A full job description, the location of the job, employing company, Job Category (i.e. engineering jobs, accounting & finance jobs etc.), the contract type ('full_time' or 'part_time') and others. The target was a normalized, annualized salary - the midpoint of the salary range provided by the employing company.

I focused on just the full job description and the job title. I cleaned this text data using Textacy and used a TFIDF Vectorizer with an n-gram range of 2-4 words, removing English stop words. I was ultimately left with a matrix of 5,000 features (2,500 for the most commonly occuring 2,3 and 4 word expressions in the full job description and 2,500 features for the same n-gram range in just the job titles).

I modeled using multiple linear regression and was able to explain 51.51% of the variance in the normalized, annualized salary using these 5,000 extracted features. 

Next steps would be to roll in different features - perhaps encoded company names and encoded locations and to build a neural network to improve the model's r squared. I might also try stemming the existing features or removing words or expressions that are abundant across all job descriptions on job sites that aren't likely to carry much signal (i.e "job originally posted").