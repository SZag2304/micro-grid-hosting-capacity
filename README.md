# ⚡ Micro-Grid Hosting Capacity Analyzer

An interactive power flow analysis tool and web dashboard designed to evaluate the hosting capacity of distribution transformers for Distributed Energy Resources (DERs). 

This project simulates a radial low-voltage (LV) feeder to determine if new residential solar installations will cause thermal overloads or voltage limit violations (Voltage Rise) on the local micro-grid.

## 🚀 Overview

As renewable energy adoption accelerates, distribution grids face bidirectional power flow challenges. This application uses **Pandapower** to run Newton-Raphson power flow simulations, evaluating the "Maximum Generation / Minimum Load" scenario to ensure grid safety and stability. 

The accompanying web dashboard, built with **Streamlit** and **Plotly**, provides an intuitive interface for grid planners to dynamically adjust parameters and visualize voltage gradients along the feeder.

## 🛠️ Features
* **Dynamic Grid Modeling:** Instantly generate radial distribution networks with configurable transformer limits and neighborhood sizes.
* **Thermal Limit Analysis:** Calculates reverse power flow to ensure transformer loading stays below 100% capacity.
* **Voltage Rise Visualization:** Identifies overvoltage violations (> 1.05 pu) caused by high solar injection over resistive lines (#2 AWG).
* **Interactive Dashboard:** A user-friendly web interface for running real-time "What-If" scenarios without touching the underlying Python code.

## ⚙️ Engineering Concepts Demonstrated
* Power Flow Analysis (Newton-Raphson)
* Grid Hosting Capacity & Siting
* Voltage Drop/Rise in AC Distribution
* Transformer Sizing & Thermal Constraints
* Renewable Integration & Export Limiting

## 💻 Tech Stack
* **Python 3**
* **Pandapower:** Power system modeling and analysis
* **Streamlit:** Interactive web application framework
* **Plotly & Pandas:** Data manipulation and advanced visualization

## 🏃‍♂️ How to Run Locally

**Prerequisites:** Ensure you have Python 3.8 or higher installed on your machine.

**1. Clone the repository** Open your terminal (or command prompt) and download the project to your local machine:
```bash
git clone https://github.com/SZag2304/micro-grid-hosting-capacity.git
```
**2. Navigate to the project folder** Change your directory to the newly downloaded folder:
```bash
cd micro-grid-hosting-capacity
```
**3. Install the required libraries** Install the necessary Python dependencies used for the simulation and the web dashboard:
```bash
pip install pandapower streamlit plotly pandas
```
**4. Launch the web application** Start the interactive Streamlit server by running:
```bash
streamlit run app.py
```
(The dashboard will automatically open in your default web browser, typically at http://localhost:8501)

## Overview
<img width="1710" height="1107" alt="1  Initial Page" src="https://github.com/user-attachments/assets/045be534-4935-43c0-aafd-a79096c49186" />
<img width="1710" height="1107" alt="2  Simulation Result   Bus Voltages" src="https://github.com/user-attachments/assets/9d82569f-8df6-48e0-baf8-7a5f650792b6" />
<img width="1710" height="1107" alt="3  Voltage Profile" src="https://github.com/user-attachments/assets/47eb1308-eded-45a6-842b-82855d897204" />
