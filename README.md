<p align="right">
  <img src="https://img.shields.io/github/issues/aman8949/VISA-Anywhere" />
  <img src="https://img.shields.io/github/forks/aman8949/VISA-Anywhere" />
  <img src="https://img.shields.io/github/stars/aman8949/VISA-Anywhere" />
</p>

# **VISA ANYWHERE**
_**Theme:** Cardholders/Consumers_

## **Introduction**:
The ongoing spread of **COVID-19** is one of the biggest threat to human life but side-by-side also becoming the tipping point for **digital payments**. To contain the impact of this pandemic, many countries are taking several measures, like nationwide lockdowns, limiting the number of people on public places, urging the public to stay indoors and maintain social distance. In such crisis, we need a medium to manage and fulfil our daily survival requirements like purchasing groceries, medicines and other essentials items in a safe and frictionless manner, that's what **VISA Anywhere** focuses on.

## **Project Description**:
With the integration of various **VISA APIs**, this project aims to prevent large gatherings of people in various stores and shops during ongoing COVID-19 pandemic and help in **promoting digital payments in a contactless and hassle-free manner**. 

This web-app basically facilitate a user to preorder various items from a **VISA Card** accepting merchant (affiliated with our web-app) around his/her location while showing wait times of that particular merchant store for which a user should actually wait before picking up the order from that merchant store and thus, avoiding the crowd and maintaining social-distancing. To make the process safer and smoother, we also provide weather insights along with the options for home delivery and multiple slot availability for ordering throughout the day as per the merchant's consent and consumers' convenience.

## Visuals & Working:
#### 1. Homepage: 
  [![README_1](https://github.com/aman8949/VISA-Anywhere/blob/master/media/shop/images/README_1.png)](http://127.0.0.1:8000/)

#### 2. Registeration Page: 
  [![README_2](https://github.com/aman8949/VISA-Anywhere/blob/master/media/shop/images/README_2.png)](http://127.0.0.1:8000/shop/register/)

#### 3. Login Page: 
  [![README_3](https://github.com/aman8949/VISA-Anywhere/blob/master/media/shop/images/README_3.png)](http://127.0.0.1:8000/shop/login/)

#### 4. Merchant list nearby the user: 
  [![README_4](https://github.com/aman8949/VISA-Anywhere/blob/master/media/shop/images/README_4.png)](http://127.0.0.1:8000/shop/register/)

#### 5. Products list from selected Merchant Store: 
  [![README_5](https://github.com/aman8949/VISA-Anywhere/blob/master/media/shop/images/README_5.png)](http://127.0.0.1:8000/shop/product_list/33)

## **Technologies Used**:
* Python
* Django framework
* HTML
* CSS
* Bootstrap
* JavaScript
* JSON
## APIs Used:
* **VISA**:
    * Merchant Locator
    * Visa Queue Insights
    * Visa Checkout
* **Third-Party**:
    * Mapbox
    * OpenWeatherMap

## **Development Setup**:
### **Getting started**:
Open Command Prompt/Terminal then follow:
 1. **Cloning the repository**:
    ```bash
    git clone https://github.com/aman8949/VISA-Anywhere
    cd .\VISA-Anywhere\
    ```
2. **Installation**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Starting Django Server**:
    ```python
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser --username=admin --email=admin@visaanywhere.com
    ```
    Now select a suitable password or set it as:
    ```python
    password: @v1i2s3a4
    ```
    If prompted to bypass, type: **y** and press **enter** else follow next step:
    ```python
    python manage.py runserver
    ```
4. **Open your browser to the following URL**:
    ```python
    http://127.0.0.1:8000/
    ```
## Acknowledgment:
This project is a part of a submission to **[Visa Global Intern Hackathon](https://www.hackerearth.com/challenges/hackathon/visa-hackathon-2020/)** for the **Innovation Challenge - Payments and the Pandemic** by the team **IIT BHU**.

* Team **IIT BHU** Members:
    * [Aman Gupta](https://github.com/aman8949)
    * [Akshita Khandelwal](https://github.com/aksh123-ui)
    * [Ayush Singh](https://github.com/adamcode26)
    * [Gaurav Singh](https://github.com/gaurav6225)
    * [Harsh Jangid](https://github.com/harshjangid)
    * [Rahul Kocheta](https://github.com/rahulkocheta)

----
