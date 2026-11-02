# MP2 Rest API

This is a FastAPI application that takes in a CSV file as an upload, stores the data, and allows users to adjust the
parameters of the processing as needed. Users can choose which file they provide as input, which rows are excluded from
the analysis, change the data validation conditions, and turn on and off various cleaning processes such as removing
duplicates and missing values. All HTTP requests are tracked and handled appropriately.