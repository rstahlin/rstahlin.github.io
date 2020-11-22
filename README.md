# DC-COVID Tracking Project
## The Project
DC releases a truly incredible amount of data every day on Covid-19. The problem? It's in a completely useless format, showing cumulative totals rather than daily changes. 

**The mission of this project is to fill that knowledge gap with interactive visualizations that help ordinary Washingtonians digest trends, risk, and inequities during the pandemic.**

I started keeping track of this data on the first day they started releasing it back in March, and it's evolved from there. What started as a Streamlit app on my local network has now, with a lot of web development help from a friend, become a Github Pages website.

## The Data
Each day around 1000 ET, DC updates an [excel file on box](https://dcgov.app.box.com/v/DCHealthStatisticsData) which I have to manually copy and paste into `data.csv` because Box's API doesn't allow downloads from shell scripts for the specific way DC shares the link (as far as I've been able to tell). This gets most of the data, but I also wait for DC and/or PoPville to post screenshots of a table that contains age data, which is remarkably not released sequentially in their spreadsheet.

Throughout the many months DC has been releasing data, there have been several (~ a dozen) copy/paste errors that I've spotted in their data. I have painstakingly corrected these to the best of my ability, but where I was unable to, I replaced those day's data with a simple average between the days before and after the error. This means you will *not* get the same results/charts if you were to recreate `data.csv` on your own (which I don't recommend anyway, because it's hard to do!). I am working on documenting these errors and will eventually post a text file documenting the fixes I have applied. Need it sooner? Let me know.

## The Charts
The python script `charts.py` grew out of `covid_streamlit.py`, the aforementioned legacy Streamlit app. As the name so cleverly suggests, it makes interactive Plotly charts and saves them to the `chart_htmls/` directly. I plan to still update this with more charts and to be more reader friendly, so be on the lookout for more updates.

## The Website
Our website, [dccovid.com](dccovid.com) is developed with a Bootstrap framework, and mainly operates by pulling the Plotly charts from `chart_htmls/` onto the `index.html`. 

## The Future
We intend to roll out more data and features onto the website, such as data tables, download links, and reopening metrics. On the data pipeline side, we also intend to explore scraping as a natural alternative to manually copying and pasting everyday. Think you've got better ideas, punk? Let us know!
