#Importation des librairies
import streamlit as st
import streamlit.components.v1 as components

from PIL import Image
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import requests
import os
import shap
import pickle

# https://projet7-credit.herokuapp.com/predict/218461
# Lecture des données
feature_names = ['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'OWN_CAR_AGE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY', 'HOUR_APPR_PROCESS_START', 'REG_REGION_NOT_LIVE_REGION', 'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY', 'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG', 'COMMONAREA_AVG', 'ELEVATORS_AVG', 'ENTRANCES_AVG', 'FLOORSMAX_AVG', 'FLOORSMIN_AVG', 'LANDAREA_AVG', 'LIVINGAPARTMENTS_AVG', 'LIVINGAREA_AVG', 'NONLIVINGAPARTMENTS_AVG', 'NONLIVINGAREA_AVG', 'APARTMENTS_MODE', 'BASEMENTAREA_MODE', 'YEARS_BEGINEXPLUATATION_MODE', 'YEARS_BUILD_MODE', 'COMMONAREA_MODE', 'ELEVATORS_MODE', 'ENTRANCES_MODE', 'FLOORSMAX_MODE', 'FLOORSMIN_MODE', 'LANDAREA_MODE', 'LIVINGAPARTMENTS_MODE', 'LIVINGAREA_MODE', 'NONLIVINGAPARTMENTS_MODE', 'NONLIVINGAREA_MODE', 'APARTMENTS_MEDI', 'BASEMENTAREA_MEDI', 'YEARS_BEGINEXPLUATATION_MEDI', 'YEARS_BUILD_MEDI', 'COMMONAREA_MEDI', 'ELEVATORS_MEDI', 'ENTRANCES_MEDI', 'FLOORSMAX_MEDI', 'FLOORSMIN_MEDI', 'LANDAREA_MEDI', 'LIVINGAPARTMENTS_MEDI', 'LIVINGAREA_MEDI', 'NONLIVINGAPARTMENTS_MEDI', 'NONLIVINGAREA_MEDI', 'TOTALAREA_MODE', 'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3', 'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6', 'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9', 'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12', 'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15', 'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18', 'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21', 'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_YEAR', 'NAME_CONTRACT_TYPE_Cash loans', 'NAME_CONTRACT_TYPE_Revolving loans', 'NAME_TYPE_SUITE_Children', 'NAME_TYPE_SUITE_Family', 'NAME_TYPE_SUITE_Group of people', 'NAME_TYPE_SUITE_Other_A', 'NAME_TYPE_SUITE_Other_B', 'NAME_TYPE_SUITE_Spouse, partner', 'NAME_TYPE_SUITE_Unaccompanied', 'NAME_INCOME_TYPE_Businessman', 'NAME_INCOME_TYPE_Commercial associate', 'NAME_INCOME_TYPE_Maternity leave', 'NAME_INCOME_TYPE_Pensioner', 'NAME_INCOME_TYPE_State servant', 'NAME_INCOME_TYPE_Student', 'NAME_INCOME_TYPE_Unemployed', 'NAME_INCOME_TYPE_Working', 'NAME_EDUCATION_TYPE_Academic degree', 'NAME_EDUCATION_TYPE_Higher education', 'NAME_EDUCATION_TYPE_Incomplete higher', 'NAME_EDUCATION_TYPE_Lower secondary', 'NAME_EDUCATION_TYPE_Secondary / secondary special', 'NAME_FAMILY_STATUS_Civil marriage', 'NAME_FAMILY_STATUS_Married', 'NAME_FAMILY_STATUS_Separated', 'NAME_FAMILY_STATUS_Single / not married', 'NAME_FAMILY_STATUS_Unknown', 'NAME_FAMILY_STATUS_Widow', 'NAME_HOUSING_TYPE_Co-op apartment', 'NAME_HOUSING_TYPE_House / apartment', 'NAME_HOUSING_TYPE_Municipal apartment', 'NAME_HOUSING_TYPE_Office apartment', 'NAME_HOUSING_TYPE_Rented apartment', 'NAME_HOUSING_TYPE_With parents', 'OCCUPATION_TYPE_Accountants', 'OCCUPATION_TYPE_Cleaning staff', 'OCCUPATION_TYPE_Cooking staff', 'OCCUPATION_TYPE_Core staff', 'OCCUPATION_TYPE_Drivers', 'OCCUPATION_TYPE_HR staff', 'OCCUPATION_TYPE_High skill tech staff', 'OCCUPATION_TYPE_IT staff', 'OCCUPATION_TYPE_Laborers', 'OCCUPATION_TYPE_Low-skill Laborers', 'OCCUPATION_TYPE_Managers', 'OCCUPATION_TYPE_Medicine staff', 'OCCUPATION_TYPE_Private service staff', 'OCCUPATION_TYPE_Realty agents', 'OCCUPATION_TYPE_Sales staff', 'OCCUPATION_TYPE_Secretaries', 'OCCUPATION_TYPE_Security staff', 'OCCUPATION_TYPE_Waiters/barmen staff', 'WEEKDAY_APPR_PROCESS_START_FRIDAY', 'WEEKDAY_APPR_PROCESS_START_MONDAY', 'WEEKDAY_APPR_PROCESS_START_SATURDAY', 'WEEKDAY_APPR_PROCESS_START_SUNDAY', 'WEEKDAY_APPR_PROCESS_START_THURSDAY', 'WEEKDAY_APPR_PROCESS_START_TUESDAY', 'WEEKDAY_APPR_PROCESS_START_WEDNESDAY', 'ORGANIZATION_TYPE_Advertising', 'ORGANIZATION_TYPE_Agriculture', 'ORGANIZATION_TYPE_Bank', 'ORGANIZATION_TYPE_Business Entity Type 1', 'ORGANIZATION_TYPE_Business Entity Type 2', 'ORGANIZATION_TYPE_Business Entity Type 3', 'ORGANIZATION_TYPE_Cleaning', 'ORGANIZATION_TYPE_Construction', 'ORGANIZATION_TYPE_Culture', 'ORGANIZATION_TYPE_Electricity', 'ORGANIZATION_TYPE_Emergency', 'ORGANIZATION_TYPE_Government', 'ORGANIZATION_TYPE_Hotel', 'ORGANIZATION_TYPE_Housing', 'ORGANIZATION_TYPE_Industry: type 1', 'ORGANIZATION_TYPE_Industry: type 10', 'ORGANIZATION_TYPE_Industry: type 11', 'ORGANIZATION_TYPE_Industry: type 12', 'ORGANIZATION_TYPE_Industry: type 13', 'ORGANIZATION_TYPE_Industry: type 2', 'ORGANIZATION_TYPE_Industry: type 3', 'ORGANIZATION_TYPE_Industry: type 4', 'ORGANIZATION_TYPE_Industry: type 5', 'ORGANIZATION_TYPE_Industry: type 6', 'ORGANIZATION_TYPE_Industry: type 7', 'ORGANIZATION_TYPE_Industry: type 8', 'ORGANIZATION_TYPE_Industry: type 9', 'ORGANIZATION_TYPE_Insurance', 'ORGANIZATION_TYPE_Kindergarten', 'ORGANIZATION_TYPE_Legal Services', 'ORGANIZATION_TYPE_Medicine', 'ORGANIZATION_TYPE_Military', 'ORGANIZATION_TYPE_Mobile', 'ORGANIZATION_TYPE_Other', 'ORGANIZATION_TYPE_Police', 'ORGANIZATION_TYPE_Postal', 'ORGANIZATION_TYPE_Realtor', 'ORGANIZATION_TYPE_Religion', 'ORGANIZATION_TYPE_Restaurant', 'ORGANIZATION_TYPE_School', 'ORGANIZATION_TYPE_Security', 'ORGANIZATION_TYPE_Security Ministries', 'ORGANIZATION_TYPE_Self-employed', 'ORGANIZATION_TYPE_Services', 'ORGANIZATION_TYPE_Telecom', 'ORGANIZATION_TYPE_Trade: type 1', 'ORGANIZATION_TYPE_Trade: type 2', 'ORGANIZATION_TYPE_Trade: type 3', 'ORGANIZATION_TYPE_Trade: type 4', 'ORGANIZATION_TYPE_Trade: type 5', 'ORGANIZATION_TYPE_Trade: type 6', 'ORGANIZATION_TYPE_Trade: type 7', 'ORGANIZATION_TYPE_Transport: type 1', 'ORGANIZATION_TYPE_Transport: type 2', 'ORGANIZATION_TYPE_Transport: type 3', 'ORGANIZATION_TYPE_Transport: type 4', 'ORGANIZATION_TYPE_University', 'ORGANIZATION_TYPE_XNA', 'FONDKAPREMONT_MODE_not specified', 'FONDKAPREMONT_MODE_org spec account', 'FONDKAPREMONT_MODE_reg oper account', 'FONDKAPREMONT_MODE_reg oper spec account', 'HOUSETYPE_MODE_block of flats', 'HOUSETYPE_MODE_specific housing', 'HOUSETYPE_MODE_terraced house', 'WALLSMATERIAL_MODE_Block', 'WALLSMATERIAL_MODE_Mixed', 'WALLSMATERIAL_MODE_Monolithic', 'WALLSMATERIAL_MODE_Others', 'WALLSMATERIAL_MODE_Panel', 'WALLSMATERIAL_MODE_Stone, brick', 'WALLSMATERIAL_MODE_Wooden', 'EMERGENCYSTATE_MODE_No', 'EMERGENCYSTATE_MODE_Yes', 'DAYS_EMPLOYED_PERC', 'INCOME_CREDIT_PERC', 'INCOME_PER_PERSON', 'ANNUITY_INCOME_PERC', 'PAYMENT_RATE', 'BURO_DAYS_CREDIT_MIN', 'BURO_DAYS_CREDIT_MAX', 'BURO_DAYS_CREDIT_MEAN', 'BURO_DAYS_CREDIT_VAR', 'BURO_DAYS_CREDIT_ENDDATE_MIN', 'BURO_DAYS_CREDIT_ENDDATE_MAX', 'BURO_DAYS_CREDIT_ENDDATE_MEAN', 'BURO_DAYS_CREDIT_UPDATE_MEAN', 'BURO_CREDIT_DAY_OVERDUE_MAX', 'BURO_CREDIT_DAY_OVERDUE_MEAN', 'BURO_AMT_CREDIT_MAX_OVERDUE_MEAN', 'BURO_AMT_CREDIT_SUM_MAX', 'BURO_AMT_CREDIT_SUM_MEAN', 'BURO_AMT_CREDIT_SUM_SUM', 'BURO_AMT_CREDIT_SUM_DEBT_MAX', 'BURO_AMT_CREDIT_SUM_DEBT_MEAN', 'BURO_AMT_CREDIT_SUM_DEBT_SUM', 'BURO_AMT_CREDIT_SUM_OVERDUE_MEAN', 'BURO_AMT_CREDIT_SUM_LIMIT_MEAN', 'BURO_AMT_CREDIT_SUM_LIMIT_SUM', 'BURO_AMT_ANNUITY_MAX', 'BURO_AMT_ANNUITY_MEAN', 'BURO_CNT_CREDIT_PROLONG_SUM', 'BURO_MONTHS_BALANCE_MIN_MIN', 'BURO_MONTHS_BALANCE_MAX_MAX', 'BURO_MONTHS_BALANCE_SIZE_MEAN', 'BURO_MONTHS_BALANCE_SIZE_SUM', 'BURO_CREDIT_ACTIVE_Active_MEAN', 'BURO_CREDIT_ACTIVE_Bad debt_MEAN', 'BURO_CREDIT_ACTIVE_Closed_MEAN', 'BURO_CREDIT_ACTIVE_Sold_MEAN', 'BURO_CREDIT_ACTIVE_nan_MEAN', 'BURO_CREDIT_CURRENCY_currency 1_MEAN', 'BURO_CREDIT_CURRENCY_currency 2_MEAN', 'BURO_CREDIT_CURRENCY_currency 3_MEAN', 'BURO_CREDIT_CURRENCY_currency 4_MEAN', 'BURO_CREDIT_CURRENCY_nan_MEAN', 'BURO_CREDIT_TYPE_Another type of loan_MEAN', 'BURO_CREDIT_TYPE_Car loan_MEAN', 'BURO_CREDIT_TYPE_Cash loan (non-earmarked)_MEAN', 'BURO_CREDIT_TYPE_Consumer credit_MEAN', 'BURO_CREDIT_TYPE_Credit card_MEAN', 'BURO_CREDIT_TYPE_Interbank credit_MEAN', 'BURO_CREDIT_TYPE_Loan for business development_MEAN', 'BURO_CREDIT_TYPE_Loan for purchase of shares (margin lending)_MEAN', 'BURO_CREDIT_TYPE_Loan for the purchase of equipment_MEAN', 'BURO_CREDIT_TYPE_Loan for working capital replenishment_MEAN', 'BURO_CREDIT_TYPE_Microloan_MEAN', 'BURO_CREDIT_TYPE_Mobile operator loan_MEAN', 'BURO_CREDIT_TYPE_Mortgage_MEAN', 'BURO_CREDIT_TYPE_Real estate loan_MEAN', 'BURO_CREDIT_TYPE_Unknown type of loan_MEAN', 'BURO_CREDIT_TYPE_nan_MEAN', 'BURO_STATUS_0_MEAN_MEAN', 'BURO_STATUS_1_MEAN_MEAN', 'BURO_STATUS_2_MEAN_MEAN', 'BURO_STATUS_3_MEAN_MEAN', 'BURO_STATUS_4_MEAN_MEAN', 'BURO_STATUS_5_MEAN_MEAN', 'BURO_STATUS_C_MEAN_MEAN', 'BURO_STATUS_X_MEAN_MEAN', 'BURO_STATUS_nan_MEAN_MEAN', 'ACTIVE_DAYS_CREDIT_MIN', 'ACTIVE_DAYS_CREDIT_MAX', 'ACTIVE_DAYS_CREDIT_MEAN', 'ACTIVE_DAYS_CREDIT_VAR', 'ACTIVE_DAYS_CREDIT_ENDDATE_MIN', 'ACTIVE_DAYS_CREDIT_ENDDATE_MAX', 'ACTIVE_DAYS_CREDIT_ENDDATE_MEAN', 'ACTIVE_DAYS_CREDIT_UPDATE_MEAN', 'ACTIVE_CREDIT_DAY_OVERDUE_MAX', 'ACTIVE_CREDIT_DAY_OVERDUE_MEAN', 'ACTIVE_AMT_CREDIT_MAX_OVERDUE_MEAN', 'ACTIVE_AMT_CREDIT_SUM_MAX', 'ACTIVE_AMT_CREDIT_SUM_MEAN', 'ACTIVE_AMT_CREDIT_SUM_SUM', 'ACTIVE_AMT_CREDIT_SUM_DEBT_MAX', 'ACTIVE_AMT_CREDIT_SUM_DEBT_MEAN', 'ACTIVE_AMT_CREDIT_SUM_DEBT_SUM', 'ACTIVE_AMT_CREDIT_SUM_OVERDUE_MEAN', 'ACTIVE_AMT_CREDIT_SUM_LIMIT_MEAN', 'ACTIVE_AMT_CREDIT_SUM_LIMIT_SUM', 'ACTIVE_CNT_CREDIT_PROLONG_SUM', 'ACTIVE_MONTHS_BALANCE_MIN_MIN', 'ACTIVE_MONTHS_BALANCE_MAX_MAX', 'ACTIVE_MONTHS_BALANCE_SIZE_MEAN', 'ACTIVE_MONTHS_BALANCE_SIZE_SUM', 'CLOSED_DAYS_CREDIT_MIN', 'CLOSED_DAYS_CREDIT_MAX', 'CLOSED_DAYS_CREDIT_MEAN', 'CLOSED_DAYS_CREDIT_VAR', 'CLOSED_DAYS_CREDIT_ENDDATE_MIN', 'CLOSED_DAYS_CREDIT_ENDDATE_MAX', 'CLOSED_DAYS_CREDIT_ENDDATE_MEAN', 'CLOSED_DAYS_CREDIT_UPDATE_MEAN', 'CLOSED_CREDIT_DAY_OVERDUE_MAX', 'CLOSED_CREDIT_DAY_OVERDUE_MEAN', 'CLOSED_AMT_CREDIT_MAX_OVERDUE_MEAN', 'CLOSED_AMT_CREDIT_SUM_MAX', 'CLOSED_AMT_CREDIT_SUM_MEAN', 'CLOSED_AMT_CREDIT_SUM_SUM', 'CLOSED_AMT_CREDIT_SUM_DEBT_MAX', 'CLOSED_AMT_CREDIT_SUM_DEBT_MEAN', 'CLOSED_AMT_CREDIT_SUM_DEBT_SUM', 'CLOSED_AMT_CREDIT_SUM_OVERDUE_MEAN', 'CLOSED_AMT_CREDIT_SUM_LIMIT_MEAN', 'CLOSED_AMT_CREDIT_SUM_LIMIT_SUM', 'CLOSED_CNT_CREDIT_PROLONG_SUM', 'CLOSED_MONTHS_BALANCE_MIN_MIN', 'CLOSED_MONTHS_BALANCE_MAX_MAX', 'CLOSED_MONTHS_BALANCE_SIZE_MEAN', 'CLOSED_MONTHS_BALANCE_SIZE_SUM', 'PREV_AMT_ANNUITY_MIN', 'PREV_AMT_ANNUITY_MAX', 'PREV_AMT_ANNUITY_MEAN', 'PREV_AMT_APPLICATION_MIN', 'PREV_AMT_APPLICATION_MAX', 'PREV_AMT_APPLICATION_MEAN', 'PREV_AMT_CREDIT_MIN', 'PREV_AMT_CREDIT_MAX', 'PREV_AMT_CREDIT_MEAN', 'PREV_APP_CREDIT_PERC_MIN', 'PREV_APP_CREDIT_PERC_MAX', 'PREV_APP_CREDIT_PERC_MEAN', 'PREV_APP_CREDIT_PERC_VAR', 'PREV_AMT_DOWN_PAYMENT_MIN', 'PREV_AMT_DOWN_PAYMENT_MAX', 'PREV_AMT_DOWN_PAYMENT_MEAN', 'PREV_AMT_GOODS_PRICE_MIN', 'PREV_AMT_GOODS_PRICE_MAX', 'PREV_AMT_GOODS_PRICE_MEAN', 'PREV_HOUR_APPR_PROCESS_START_MIN', 'PREV_HOUR_APPR_PROCESS_START_MAX', 'PREV_HOUR_APPR_PROCESS_START_MEAN', 'PREV_RATE_DOWN_PAYMENT_MIN', 'PREV_RATE_DOWN_PAYMENT_MAX', 'PREV_RATE_DOWN_PAYMENT_MEAN', 'PREV_DAYS_DECISION_MIN', 'PREV_DAYS_DECISION_MAX', 'PREV_DAYS_DECISION_MEAN', 'PREV_CNT_PAYMENT_MEAN', 'PREV_CNT_PAYMENT_SUM', 'PREV_NAME_CONTRACT_TYPE_Cash loans_MEAN', 'PREV_NAME_CONTRACT_TYPE_Consumer loans_MEAN', 'PREV_NAME_CONTRACT_TYPE_Revolving loans_MEAN', 'PREV_NAME_CONTRACT_TYPE_XNA_MEAN', 'PREV_NAME_CONTRACT_TYPE_nan_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_FRIDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_MONDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_SATURDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_SUNDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_THURSDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_TUESDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_WEDNESDAY_MEAN', 'PREV_WEEKDAY_APPR_PROCESS_START_nan_MEAN', 'PREV_FLAG_LAST_APPL_PER_CONTRACT_N_MEAN', 'PREV_FLAG_LAST_APPL_PER_CONTRACT_Y_MEAN', 'PREV_FLAG_LAST_APPL_PER_CONTRACT_nan_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Building a house or an annex_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Business development_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Buying a garage_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Buying a holiday home / land_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Buying a home_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Buying a new car_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Buying a used car_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Car repairs_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Education_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Everyday expenses_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Furniture_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Gasification / water supply_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Hobby_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Journey_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Medicine_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Money for a third person_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Other_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Payments on other loans_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Purchase of electronic equipment_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Refusal to name the goal_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Repairs_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Urgent needs_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_Wedding / gift / holiday_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_XAP_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_XNA_MEAN', 'PREV_NAME_CASH_LOAN_PURPOSE_nan_MEAN', 'PREV_NAME_CONTRACT_STATUS_Approved_MEAN', 'PREV_NAME_CONTRACT_STATUS_Canceled_MEAN', 'PREV_NAME_CONTRACT_STATUS_Refused_MEAN', 'PREV_NAME_CONTRACT_STATUS_Unused offer_MEAN', 'PREV_NAME_CONTRACT_STATUS_nan_MEAN', 'PREV_NAME_PAYMENT_TYPE_Cash through the bank_MEAN', 'PREV_NAME_PAYMENT_TYPE_Cashless from the account of the employer_MEAN', 'PREV_NAME_PAYMENT_TYPE_Non-cash from your account_MEAN', 'PREV_NAME_PAYMENT_TYPE_XNA_MEAN', 'PREV_NAME_PAYMENT_TYPE_nan_MEAN', 'PREV_CODE_REJECT_REASON_CLIENT_MEAN', 'PREV_CODE_REJECT_REASON_HC_MEAN', 'PREV_CODE_REJECT_REASON_LIMIT_MEAN', 'PREV_CODE_REJECT_REASON_SCO_MEAN', 'PREV_CODE_REJECT_REASON_SCOFR_MEAN', 'PREV_CODE_REJECT_REASON_SYSTEM_MEAN', 'PREV_CODE_REJECT_REASON_VERIF_MEAN', 'PREV_CODE_REJECT_REASON_XAP_MEAN', 'PREV_CODE_REJECT_REASON_XNA_MEAN', 'PREV_CODE_REJECT_REASON_nan_MEAN', 'PREV_NAME_TYPE_SUITE_Children_MEAN', 'PREV_NAME_TYPE_SUITE_Family_MEAN', 'PREV_NAME_TYPE_SUITE_Group of people_MEAN', 'PREV_NAME_TYPE_SUITE_Other_A_MEAN', 'PREV_NAME_TYPE_SUITE_Other_B_MEAN', 'PREV_NAME_TYPE_SUITE_Spouse, partner_MEAN', 'PREV_NAME_TYPE_SUITE_Unaccompanied_MEAN', 'PREV_NAME_TYPE_SUITE_nan_MEAN', 'PREV_NAME_CLIENT_TYPE_New_MEAN', 'PREV_NAME_CLIENT_TYPE_Refreshed_MEAN', 'PREV_NAME_CLIENT_TYPE_Repeater_MEAN', 'PREV_NAME_CLIENT_TYPE_XNA_MEAN', 'PREV_NAME_CLIENT_TYPE_nan_MEAN', 'PREV_NAME_GOODS_CATEGORY_Additional Service_MEAN', 'PREV_NAME_GOODS_CATEGORY_Animals_MEAN', 'PREV_NAME_GOODS_CATEGORY_Audio/Video_MEAN', 'PREV_NAME_GOODS_CATEGORY_Auto Accessories_MEAN', 'PREV_NAME_GOODS_CATEGORY_Clothing and Accessories_MEAN', 'PREV_NAME_GOODS_CATEGORY_Computers_MEAN', 'PREV_NAME_GOODS_CATEGORY_Construction Materials_MEAN', 'PREV_NAME_GOODS_CATEGORY_Consumer Electronics_MEAN', 'PREV_NAME_GOODS_CATEGORY_Direct Sales_MEAN', 'PREV_NAME_GOODS_CATEGORY_Education_MEAN', 'PREV_NAME_GOODS_CATEGORY_Fitness_MEAN', 'PREV_NAME_GOODS_CATEGORY_Furniture_MEAN', 'PREV_NAME_GOODS_CATEGORY_Gardening_MEAN', 'PREV_NAME_GOODS_CATEGORY_Homewares_MEAN', 'PREV_NAME_GOODS_CATEGORY_House Construction_MEAN', 'PREV_NAME_GOODS_CATEGORY_Insurance_MEAN', 'PREV_NAME_GOODS_CATEGORY_Jewelry_MEAN', 'PREV_NAME_GOODS_CATEGORY_Medical Supplies_MEAN', 'PREV_NAME_GOODS_CATEGORY_Medicine_MEAN', 'PREV_NAME_GOODS_CATEGORY_Mobile_MEAN', 'PREV_NAME_GOODS_CATEGORY_Office Appliances_MEAN', 'PREV_NAME_GOODS_CATEGORY_Other_MEAN', 'PREV_NAME_GOODS_CATEGORY_Photo / Cinema Equipment_MEAN', 'PREV_NAME_GOODS_CATEGORY_Sport and Leisure_MEAN', 'PREV_NAME_GOODS_CATEGORY_Tourism_MEAN', 'PREV_NAME_GOODS_CATEGORY_Vehicles_MEAN', 'PREV_NAME_GOODS_CATEGORY_Weapon_MEAN', 'PREV_NAME_GOODS_CATEGORY_XNA_MEAN', 'PREV_NAME_GOODS_CATEGORY_nan_MEAN', 'PREV_NAME_PORTFOLIO_Cards_MEAN', 'PREV_NAME_PORTFOLIO_Cars_MEAN', 'PREV_NAME_PORTFOLIO_Cash_MEAN', 'PREV_NAME_PORTFOLIO_POS_MEAN', 'PREV_NAME_PORTFOLIO_XNA_MEAN', 'PREV_NAME_PORTFOLIO_nan_MEAN', 'PREV_NAME_PRODUCT_TYPE_XNA_MEAN', 'PREV_NAME_PRODUCT_TYPE_walk-in_MEAN', 'PREV_NAME_PRODUCT_TYPE_x-sell_MEAN', 'PREV_NAME_PRODUCT_TYPE_nan_MEAN', 'PREV_CHANNEL_TYPE_AP+ (Cash loan)_MEAN', 'PREV_CHANNEL_TYPE_Car dealer_MEAN', 'PREV_CHANNEL_TYPE_Channel of corporate sales_MEAN', 'PREV_CHANNEL_TYPE_Contact center_MEAN', 'PREV_CHANNEL_TYPE_Country-wide_MEAN', 'PREV_CHANNEL_TYPE_Credit and cash offices_MEAN', 'PREV_CHANNEL_TYPE_Regional / Local_MEAN', 'PREV_CHANNEL_TYPE_Stone_MEAN', 'PREV_CHANNEL_TYPE_nan_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Auto technology_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Clothing_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Connectivity_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Construction_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Consumer electronics_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Furniture_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Industry_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Jewelry_MEAN', 'PREV_NAME_SELLER_INDUSTRY_MLM partners_MEAN', 'PREV_NAME_SELLER_INDUSTRY_Tourism_MEAN', 'PREV_NAME_SELLER_INDUSTRY_XNA_MEAN', 'PREV_NAME_SELLER_INDUSTRY_nan_MEAN', 'PREV_NAME_YIELD_GROUP_XNA_MEAN', 'PREV_NAME_YIELD_GROUP_high_MEAN', 'PREV_NAME_YIELD_GROUP_low_action_MEAN', 'PREV_NAME_YIELD_GROUP_low_normal_MEAN', 'PREV_NAME_YIELD_GROUP_middle_MEAN', 'PREV_NAME_YIELD_GROUP_nan_MEAN', 'PREV_PRODUCT_COMBINATION_Card Street_MEAN', 'PREV_PRODUCT_COMBINATION_Card X-Sell_MEAN', 'PREV_PRODUCT_COMBINATION_Cash_MEAN', 'PREV_PRODUCT_COMBINATION_Cash Street: high_MEAN', 'PREV_PRODUCT_COMBINATION_Cash Street: low_MEAN', 'PREV_PRODUCT_COMBINATION_Cash Street: middle_MEAN', 'PREV_PRODUCT_COMBINATION_Cash X-Sell: high_MEAN', 'PREV_PRODUCT_COMBINATION_Cash X-Sell: low_MEAN', 'PREV_PRODUCT_COMBINATION_Cash X-Sell: middle_MEAN', 'PREV_PRODUCT_COMBINATION_POS household with interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS household without interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS industry with interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS industry without interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS mobile with interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS mobile without interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS other with interest_MEAN', 'PREV_PRODUCT_COMBINATION_POS others without interest_MEAN', 'PREV_PRODUCT_COMBINATION_nan_MEAN', 'APPROVED_AMT_ANNUITY_MIN', 'APPROVED_AMT_ANNUITY_MAX', 'APPROVED_AMT_ANNUITY_MEAN', 'APPROVED_AMT_APPLICATION_MIN', 'APPROVED_AMT_APPLICATION_MAX', 'APPROVED_AMT_APPLICATION_MEAN', 'APPROVED_AMT_CREDIT_MIN', 'APPROVED_AMT_CREDIT_MAX', 'APPROVED_AMT_CREDIT_MEAN', 'APPROVED_APP_CREDIT_PERC_MIN', 'APPROVED_APP_CREDIT_PERC_MAX', 'APPROVED_APP_CREDIT_PERC_MEAN', 'APPROVED_APP_CREDIT_PERC_VAR', 'APPROVED_AMT_DOWN_PAYMENT_MIN', 'APPROVED_AMT_DOWN_PAYMENT_MAX', 'APPROVED_AMT_DOWN_PAYMENT_MEAN', 'APPROVED_AMT_GOODS_PRICE_MIN', 'APPROVED_AMT_GOODS_PRICE_MAX', 'APPROVED_AMT_GOODS_PRICE_MEAN', 'APPROVED_HOUR_APPR_PROCESS_START_MIN', 'APPROVED_HOUR_APPR_PROCESS_START_MAX', 'APPROVED_HOUR_APPR_PROCESS_START_MEAN', 'APPROVED_RATE_DOWN_PAYMENT_MIN', 'APPROVED_RATE_DOWN_PAYMENT_MAX', 'APPROVED_RATE_DOWN_PAYMENT_MEAN', 'APPROVED_DAYS_DECISION_MIN', 'APPROVED_DAYS_DECISION_MAX', 'APPROVED_DAYS_DECISION_MEAN', 'APPROVED_CNT_PAYMENT_MEAN', 'APPROVED_CNT_PAYMENT_SUM', 'REFUSED_AMT_ANNUITY_MIN', 'REFUSED_AMT_ANNUITY_MAX', 'REFUSED_AMT_ANNUITY_MEAN', 'REFUSED_AMT_APPLICATION_MIN', 'REFUSED_AMT_APPLICATION_MAX', 'REFUSED_AMT_APPLICATION_MEAN', 'REFUSED_AMT_CREDIT_MIN', 'REFUSED_AMT_CREDIT_MAX', 'REFUSED_AMT_CREDIT_MEAN', 'REFUSED_APP_CREDIT_PERC_MIN', 'REFUSED_APP_CREDIT_PERC_MAX', 'REFUSED_APP_CREDIT_PERC_MEAN', 'REFUSED_AMT_GOODS_PRICE_MIN', 'REFUSED_AMT_GOODS_PRICE_MAX', 'REFUSED_AMT_GOODS_PRICE_MEAN', 'REFUSED_HOUR_APPR_PROCESS_START_MIN', 'REFUSED_HOUR_APPR_PROCESS_START_MAX', 'REFUSED_HOUR_APPR_PROCESS_START_MEAN', 'REFUSED_DAYS_DECISION_MIN', 'REFUSED_DAYS_DECISION_MAX', 'REFUSED_DAYS_DECISION_MEAN', 'REFUSED_CNT_PAYMENT_MEAN', 'REFUSED_CNT_PAYMENT_SUM', 'POS_MONTHS_BALANCE_MAX', 'POS_MONTHS_BALANCE_MEAN', 'POS_MONTHS_BALANCE_SIZE', 'POS_SK_DPD_MAX', 'POS_SK_DPD_MEAN', 'POS_SK_DPD_DEF_MAX', 'POS_SK_DPD_DEF_MEAN', 'POS_NAME_CONTRACT_STATUS_Active_MEAN', 'POS_NAME_CONTRACT_STATUS_Amortized debt_MEAN', 'POS_NAME_CONTRACT_STATUS_Approved_MEAN', 'POS_NAME_CONTRACT_STATUS_Canceled_MEAN', 'POS_NAME_CONTRACT_STATUS_Completed_MEAN', 'POS_NAME_CONTRACT_STATUS_Demand_MEAN', 'POS_NAME_CONTRACT_STATUS_Returned to the store_MEAN', 'POS_NAME_CONTRACT_STATUS_Signed_MEAN', 'POS_NAME_CONTRACT_STATUS_XNA_MEAN', 'POS_NAME_CONTRACT_STATUS_nan_MEAN', 'POS_COUNT', 'INSTAL_NUM_INSTALMENT_VERSION_NUNIQUE', 'INSTAL_DPD_MAX', 'INSTAL_DPD_MEAN', 'INSTAL_DPD_SUM', 'INSTAL_DBD_MAX', 'INSTAL_DBD_MEAN', 'INSTAL_DBD_SUM', 'INSTAL_PAYMENT_PERC_MAX', 'INSTAL_PAYMENT_PERC_MEAN', 'INSTAL_PAYMENT_PERC_SUM', 'INSTAL_PAYMENT_PERC_VAR', 'INSTAL_PAYMENT_DIFF_MAX', 'INSTAL_PAYMENT_DIFF_MEAN', 'INSTAL_PAYMENT_DIFF_SUM', 'INSTAL_PAYMENT_DIFF_VAR', 'INSTAL_AMT_INSTALMENT_MAX', 'INSTAL_AMT_INSTALMENT_MEAN', 'INSTAL_AMT_INSTALMENT_SUM','INSTAL_AMT_PAYMENT_MIN','INSTAL_AMT_PAYMENT_MAX','INSTAL_AMT_PAYMENT_MEAN','INSTAL_AMT_PAYMENT_SUM','INSTAL_DAYS_ENTRY_PAYMENT_MAX','INSTAL_DAYS_ENTRY_PAYMENT_MEAN','INSTAL_DAYS_ENTRY_PAYMENT_SUM','INSTAL_COUNT']

# Lecture du modèle
# clf_pipe = pickle.load(open('modele_final_Lightgbm_bank.md', 'rb'))

# Initialisation des algo : n plus proches voisins? pour comparaison avec autres clients
# Interprétation du modèle SHAP

# Dasboard avec streamlit

#img = Image.open("https://www.faire-un-credit.fr/wp-content/uploads/2021/02/faire-un-credit-en-ligne.png") 
#st.image(img, width=200) 
threshold = 0.5538
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

def get_top_columns(shap_vals, index, f_names, num):
    l = []
    # https://github.com/slundberg/shap/issues/632
    for name in np.flip(np.argsort(np.abs(shap_vals[index]))[-num:]):
        l.append(f_names[name])
    return l

base_path = "/app/projet7-credit/streamlit"
# base_path = os.getcwd()
expected_value = [0.7219468377624242, -0.7219468377624242]
with open(base_path + '/shap/shap_values.shap', "rb") as input_file:
  shap_values = pickle.load(input_file)
sample = pd.read_csv(base_path + '/model/app_sample.csv')
sample = sample.reset_index()
image = Image.open(base_path + '/shap/distribution.png')

#Textes
st.header("Scoring crédit client")
st.subheader("1. Prédiction de la solvabilité d'un client pour l'obtention d'un crédit")

#champ identifiant client
st.text("Veuillez saisir l'identifiant du client. Ex : 437649, 418553, 274738...")
name = st.text_input("", "Numéro d'identifiant") 
  
if(st.button('Envoyez')): 
    client_id = name.title() 
    response = requests.get("https://projet7-credit.herokuapp.com/predict/"+client_id)
    # https://community.plotly.com/t/plotly-js-gauge-pie-chart-data-order/8686
    # https://gist.github.com/tvst/b7bc2cb257ed88557037cb46e4baf80b
    zero_proba = response.json()["score"][0]
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = response.json()["score"][0],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Score"},
    gauge= { 'axis': {'range':[0,1]}}))

    if(zero_proba > threshold):
        st.success("{:.2%}".format(zero_proba) + " de probabilité de remboursement.")
        fig.update_traces(gauge_bar_color="green")
    else:
        fig.update_traces(gauge_bar_color="red")
        st.error("{:.2%}".format(1 - zero_proba)+ " de probabilité de défaut de paiement.")

    st.write(fig)
    start = int(sample[sample["SK_ID_CURR"] == int(client_id)]["index"])
    end = start + 1
    st_shap(shap.plots.force(expected_value[0], shap_values[start], feature_names))
    fig, ax = plt.subplots()
    shap.plots._waterfall.waterfall_legacy(expected_value[0], shap_values[start], feature_names=feature_names)
    st.pyplot(fig, bbox_inches='tight',dpi=300,pad_inches=0)
    plt.clf()
    st.image(image, caption='L\'importance de chaque caractéristique dans la décision')
    
    top_cols = get_top_columns(shap_values, start, feature_names, 10)
    fig, ax = plt.subplots()
    fig.set_figwidth(30)
    fig.set_figheight(10)
    sns.boxplot(data=sample[top_cols])
    sns.stripplot(data=sample[sample["SK_ID_CURR"] == int(client_id)][top_cols], color='red')
    st.pyplot(fig, bbox_inches='tight',dpi=300,pad_inches=0)
    plt.clf()
    
# faire une jauge
# N° client, crédit accepté ou non, score détaillé sous forme de jauge colorée 
# selon qu’il est en dessous ou au-dessus du seuil : 
#permet de juger s’il est loin du seuil ou non.

st.subheader("2. Influence des variables sur le score du client– TOP 10")


# Divers messages :
# st.success("Success") 
  
# st.info("Information") 
  
# st.warning("Warning") 
  
# st.error("Error") 

# Sa feature importance locale sous forme de graphique, 
#qui permet au chargé d’étude de comprendre quelles sont les données du client
# qui ont le plus influencé le calcul de son score


# Liste déroulante
feature = st.selectbox("features: ", 
                     ['Genre', 'Salaire', 'Type de logement']) 
  
st.write("Your feature: ", feature) 

# Le tableau de bord présentera également d’autres graphiques 
# sur les autres clients :
# 2 graphiques de features sélectionnées dans une liste déroulante, 
#présentant la distribution de la feature selon les classes, 
#ainsi que le positionnement de la valeur du client
# 	Un graphique d’analyse bi-variée entre les deux features sélectionnées, 
#avec un dégradé de couleur selon le score des clients, 
#et le positionnement du client
# 	La feature importance globale
# 	D’autres graphiques complémentaires
