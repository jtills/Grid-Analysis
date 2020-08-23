# Grid-Analysis

Compare local and national UK carbon intensity data for a span of up to 14 days

## Sources

National Grid's Carbon Intensity API:

https://carbonintensity.org.uk/

https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0

## Usage
User specifies start date, end date and outward postcode. 

The program returns average statistics for the region and the UK, plotting a value for every half an hour in the given time period. It also returns a line plot, subplots and a stacked plot for both the region and nationally to compare. 

Currently only displaying the green energy sources to compare to carbon intensity values, but this can be changed manually in the code.

## Improvements

How I would improve this project:
          
1. Performance: Use Numpy package to extract data more efficiently (if possible)
2. User Interface: Create user input that lets user choose which energy source(s) to analyse and adjusts graphs accordingly
3. Data Visualization:
    1. Major and minor ticks on the x-axis that avoid repetition, displaying only significant changes in time and adjusting depending on time range
    2. Allow event handling and picking to easily take values from the graphs
    
 ## Output

![](/images/Statistics.JPG)

![](/images/main.JPG)

![](/images/subplots.JPG)

![](/images/stackedplots.JPG)
