Title: Get to know your data
Date: 2021-09-17


An excel file with data has been sent to you for some cleaning the person who sent it tells you its "relatively clean, its only the amount column that is mess" Do you believe them



Well, in a small sized file it would be easy to confirm what have been told about the the status of the file. However, iif the file spans more than a few thousands rows then you are in afor a ride. Despite the good intentions of telling you the status of the file, without being told about the 1) how the data was gathered, 2) why it was gathered and 3) If any data cleaning/processing as been on the data you need to assume that you have messy data.



Data profiling can be very helpful in such a situation.  We really like the definition of data profiling as provided by [Kimball](http://www.kimballgroup.com/wp-content/uploads/2012/05/DT59SurprisingValue.pdf) as "the systematic up front analysis of the content of a data source".   



Detre does profile the data you upload. The profile is done on each column. The table below shows what the results provided for each data type.  As shown, the profile for each column is grouped into : a) summary statistics, b) outliers and c) patterns.  