
<div align="center">

# 🕵️ allben-insider-threat-detector

### *AI-Powered Behavioural Anomaly Detection for Enterprise Security*

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://allben-insider-threat-detector.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**A production-grade insider threat detection platform built by [Allben Rakgoale](https://github.com/allben09) that combines behavioural biometrics with unsupervised Machine Learning to identify malicious insiders before they cause damage.**

[🌐 Live Demo](https://allben-insider-threat-detector.streamlit.app/) · [📊 Architecture](#-architecture) · [🚀 Quick Start](#-quick-start) · [🧠 ML Model](#-ml-model-details) · [📸 Screenshots](#-screenshots)

---

### 🌐 **Try the Live Dashboard**

👉 **[https://allben-insider-threat-detector.streamlit.app](https://allben-insider-threat-detector.streamlit.app/)**

> ⚠️ **Demo Note:** This dashboard uses **simulated employee behaviour data** (50–200 employees, 90 days) with injected insider threat scenarios. The full pipeline works identically with real enterprise telemetry.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [The Insider Threat Problem](#-the-insider-threat-problem)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [ML Model Details](#-ml-model-details)
- [Threat Profiles Detected](#-threat-profiles-detected)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Docker Deployment](#-docker-deployment)
- [Cloud Deployment](#-cloud-deployment)
- [Screenshots](#-screenshots)
- [Metrics & Performance](#-metrics--performance)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🔍 Overview

**allben-insider-threat-detector** is an enterprise-grade security platform that identifies malicious insiders using **behavioural biometrics** and **unsupervised Machine Learning**. Unlike traditional rule-based systems, this platform learns what *normal* behaviour looks like for each employee and flags deviations that could indicate:

- 🔴 **Data exfiltration** — massive data transfers to unauthorised destinations
- 🔴 **Privilege escalation** — accessing sensitive files beyond job scope
- 🔴 **Off-hours access** — logging in at 2 AM when the office is empty
- 🔴 **USB abuse** — copying sensitive data to removable media
- 🔴 **Credential compromise** — unusual login patterns

Built specifically with the **South African financial sector** in mind, where insider threats are one of the top three causes of data breaches.

---

## 🎯 The Insider Threat Problem

> *"Insider threats cost organisations an average of R250 million per incident — and take 287 days to detect."*  
> — IBM Cost of a Data Breach Report

| Challenge | Why Traditional Systems Fail |
| :--- | :--- |
| **Insiders have valid credentials** | Rules can't distinguish malicious from legitimate access |
| **Behaviour is context-dependent** | What's abnormal for HR is normal for IT |
| **Signature-based detection is useless** | Insiders don't use malware — they use their own login |
| **Volume of legitimate actions is huge** | 99.9% of activity is normal |

**Solution:** Unsupervised ML that learns *each employee's* baseline behaviour and detects anomalies without needing labelled attack data.

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🧠 AI Detection Layer

- **Ensemble model**: Isolation Forest + One-Class SVM
- **Behavioural feature engineering**: 19 features per user
- **Unsupervised learning**: No labelled data required
- **Weighted risk scoring**: 0–100% confidence scale
- **Configurable sensitivity**: Adjust detection threshold

</td>
<td width="50%">

### 📊 Visualisation Layer

- **Real-time KPI dashboard**: 4 executive metrics
- **Risk distribution histogram**: Threats vs. normals
- **Top 10 suspicious users** table
- **Department risk breakdown**
- **Behavioural comparison charts**
- **CSV report export**

</td>
</tr>
<tr>
<td width="50%">

### 🎭 Simulated Attack Scenarios

- **Data exfiltration** (5–15x normal transfer)
- **Privilege escalation** (4x sensitive file access)
- **Off-hours access** (1 AM – 5 AM logins)
- **USB abuse** (3–10 events per day)
- **Realistic baseline**: 90 days per employee

</td>
<td width="50%">

### 🚀 Production-Ready

- **Streamlit Cloud** deployed
- **Dockerised** for one-command deployment
- **Environment-aware** (cloud vs. local)
- **Auto-scaling** to 200+ employees
- **Sub-second inference** on full dataset

</td>
</tr>
</table>

---

## 🏗️ Architecture
