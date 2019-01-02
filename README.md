
# Data Collection and Analysis for smart-phones/tablets and smartwatches.


## Author: Sarang Zambare

### Note: You can do whatever you want with the csv files generated in this project, no licencing involved.

This repository is for data collection and analysis of smart-devices(smartphones, tablets, watches).

The data are scraped from https://www.gsmarena.com. As of the current time, it involves 15 features namely:

1. Product Name
2. LTE or not (binary)
3. Year announced
4. Weight (in grams)
5. Display type (three types: LCD, OLED, OTHER)
6. Display size
7. PPI (Pixels Per Inch)
8. CPU (in GHz)
9. Internal memory (in GB)
10. RAM (in GB)
11. Rear Camera (in MP)
12. Front Camera (in MP)
13. Bluetooth Version
14. Battery (in mAh)
15. Price (in USD)*

* Some prices listed on the website were in foreign currencies, the appropriate current exchange rate has been applied to convert the prices to USD (as of 12/30/2018)

Currently, I am aiming at about 2000 devices (inclusive of smartphones, tablets and watches), from about 40 manufacturers.

### This is a living repository and I plan to :

- Generate a well documented dataset summarising the above mentioned features for over 2000 devices.
- Employ various supervised regression techniques like linear, natural splines, including tree-based methods like random-forests.
- Use this as an educational dataset to experiment with validation techniques like cross-validation and bootstrap.
- Explore patterns in the data by employing unsupervised techniques like PCA and Clustering.

So far, I have achieved to scrap,clean and compile into csv, data for more than 1000 phones/tablets/watches. Attaching a screenshot of the clean csv :

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/csv_shot.png)


## Note: For all the plots below, the R code and the console output of RStudio can be found in the R_dump_xx.dat files.
Below are the plots of price vs each column. Visually we can determine columns which take up most and least amount of variance in the data.

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/plot1.png)

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/plot_2.png)

Trial: Regressing price over cpu_ghz. Single variable regression.

### Linear and Quadratic regression over cpu_ghz:

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/plot_3.png)

Adjusted R-squared values indicate that the linear model explains about 29% of the total variance, whereas the quadratic model explains 43% of the total variance, as below:

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/r_squared.jpg)

### Fitting smoothing splines over three features: cpu, screen_size and ppi.

Using only three, and highly noisy features results in a pathetic fit with high error bars, especially towards the endpoints. The resulting fit had an atrociously high AIC index of 15828.6 (refer R_dump_1.dat). But we can visualise the trend of the dependence of each of the three variables, through the plots below:

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/splines.png)


### Training Random Forests over all features :

Here I train a random forest over all 13 features of the data. Using 4 features at each split of the tree, we get a **70.65% explanation of the total varaiance, which is not bad!** (refer R_dump_randomForest.dat for detailed console output)

In a different approach, the data set is divided into a training set (900 entries) and a test set (300 entries). To have a better judgement of how many features to consider at each split, the *Out of bag error* and *Test error* are plotted for different value of features:

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/rforest.png)
