
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

Adjusted R-squared values indicate that the linear model explains about **29% of the total variance**, whereas the quadratic model explains **43% of the total variance**, as below:

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/r_squared.jpg)

### Fitting smoothing splines over three features: cpu, screen_size and ppi.

```
require(gam)

gam1 = gam(price~s(cpu_ghz,df=4)+s(ppi,df=4)+s(screen_size,df=4),data=data)
summary(gam1)
Call: gam(formula = price ~ s(cpu_ghz, df = 4) + s(ppi, df = 4) + s(screen_size,
    df = 4), data = data)
Deviance Residuals:
    Min      1Q  Median      3Q     Max
-337.16  -75.08  -23.70   49.56 1264.79

(Dispersion Parameter for gaussian family taken to be 18835.41)

    Null Deviance: 47336465 on 1246 degrees of freedom
Residual Deviance: 23242893 on 1234 degrees of freedom
AIC: 15828.6
```

Using only three, and highly noisy features results in a pathetic fit with high error bars, especially towards the endpoints. The resulting fit had an atrociously high **AIC index of 15828.6** (refer R_dump_1.dat). But we can visualise the trend of the dependence of each of the three variables, through the plots below:

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/splines.png)


### Training Random Forests over all features :

Here I train a random forest over all 13 features of the data. Using 4 features at each split of the tree, we get a **70.65% explanation of the total varaiance, which is not bad!** (refer R_dump_randomForest.dat for detailed console output)

```
> data=read.csv('data_clean.csv')
> attach(data)
> require(randomForest)
> train = sample(1:nrow(data),900)
> rf.data = randomForest(price~.-name-price_category,data=data,subset=train)
> oob.err=double(13)
> test.err=double(13)

> rf.data

Call:
 randomForest(formula = price ~ . - name - price_category, data = data)
               Type of random forest: regression
                     Number of trees: 500
No. of variables tried at each split: 4

          Mean of squared residuals: 11141.51
                    % Var explained: 70.65
```                    

In a different approach, the data set is divided into a training set (900 entries) and a test set (300 entries). To have a better judgement of how many features to consider at each split, the *Out of bag error* and *Test error* are plotted for different value of features:

```
> for(mtry in 1:13){
+     fit=randomForest(price~.-name-price_category,data=data,subset=train,mtry=mtry,ntree=500)
+     oob.err[mtry] = fit$mse[500]
+     pred=predict(fit,data[-train,])
+     test.err[mtry]=with(data[-train,],mean((price-pred)^2))
+     cat(mtry," ")
+ }
1  2  3  4  5  6  7  8  9  10  11  12  13  
> matplot(1:mtry,cbind(test.err,oob.err),pch=19,col=c('red','blue'),type='b',ylab='Mean Squared Error',xlab='# of features at each split')
> legend("topright",legend=c("Out of bag","Test"),pch=19,col=c("red","blue"))
```

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/rforest.png)


Looks like in this case the OOB error does not do a decent job in predicting the test error. Also, there is not a lot of change in the test error for anything between 4 and 8 features at each split. Hence I keep it at 4 (simpler the better).


### Classification: Linear Discriminant Analysis over all features.

For the purpose of classification. I divided the devices into three classes:

1. **Cheap devices: costing $200 or less**
2. **Not-so-cheap devices: costing between $200 - $500**
3. **Expensive devices: costing $500 and above**


The aim here is to use LDA to classify devices into their respective categories. After employing LDA for the three classes (labelled as 1,2,3), the classification along each of the Linear Discriminants can be plotted as a graph : (three classes so 2 discriminants):

![alt text](https://raw.githubusercontent.com/sarangzambare/smartdevices_pricing/master/png/lda_1.png)

We can also see the confusion matrix, which gives us a better understanding of how well the model performed:

```
  1   2   3
1 103  40   1
2  34 121  12
3   0  16  20

```

The confusion matrix is tending towards being diagonal, which means the model preformed pretty well. We can also see the mean rate of correct classification, which can be a measure of the test accuracy.

```
> mean(lda.pred$class==data[-train,]$price_category)
[1] 0.70317

```

**70.31% times, the model correctly classified the devices, which is pretty good for such a dumb model!**
