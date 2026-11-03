# 🏥 RiskLens

An end-to-end machine learning application that predicts an individual's **insurance premium category** based on demographic, lifestyle, financial, and location-related factors.

The project combines a trained machine learning model with a **FastAPI backend** and **Streamlit frontend**, allowing users to enter their details and receive a predicted premium category.

## 📌 Project Overview

Insurance providers need to assess the potential risk associated with different applicants when determining appropriate premium levels. This project uses machine learning to estimate an applicant's premium category from features such as:

- Age
- Weight and height
- Smoking status
- Income
- City
- Occupation

The application derives additional features such as **BMI, lifestyle risk, age group, and city tier** before passing the processed data to the machine learning model.

## ⚙️ How It Works

```text
User Input
    ↓
Streamlit Frontend
    ↓
FastAPI API
    ↓
Feature Engineering
    ↓
Trained ML Model
    ↓
Predicted Premium Category
```

The FastAPI backend validates the user's input using Pydantic and creates the features required by the trained model.

The model receives:

- `bmi`
- `age_group`
- `lifestyle_risk`
- `city_tier`
- `income_lpa`
- `occupation`

and returns the predicted premium category.

## 🧠 Feature Engineering

### BMI

BMI is calculated from the applicant's weight and height:

```text
BMI = weight / height²
```

### Lifestyle Risk

The application derives a lifestyle risk category using smoking status and BMI:

- **High** → Smoker + BMI > 30
- **Medium** → Smoker OR BMI > 27
- **Low** → Otherwise

### Age Group

Applicants are categorized into:

- Young
- Adult
- Middle-aged
- Senior

### City Tier

Cities are categorized into Tier 1, Tier 2, or Tier 3 based on predefined city groups.

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **Scikit-learn**
- **FastAPI**
- **Pydantic**
- **Streamlit**
- **Pickle**
- **Requests**

## 🖥️ Application

The Streamlit frontend provides an interactive form where users can enter their age, weight, height, income, smoking status, city, and occupation.

The frontend sends these details to the FastAPI `/predict` endpoint and displays the resulting premium category.

## 🚀 Running the Project

### 1. Start the FastAPI Backend

```bash
python -m uvicorn app:app --reload
```

### 2. Start the Streamlit Frontend

```bash
streamlit run frontend.py
```

Make sure the FastAPI backend is running on:

```text
http://127.0.0.1:8000
```

The Streamlit application sends prediction requests to the `/predict` endpoint.

## 🎯 Project Objective

The objective of this project is to demonstrate how a machine learning model can be integrated into a practical application using **FastAPI for model serving** and **Streamlit for the user interface**, creating an end-to-end ML prediction system.

## ⚠️ Disclaimer

This project is intended for **educational and demonstration purposes only**. The predictions should not be used as a substitute for professional insurance underwriting or financial/medical advice.
