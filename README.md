# 🤖 Machine N

### *Find high-quality leads around the corner — powered by intelligent automation*

---

## 🚀 Overview

**Machine N** is an AI-powered lead generation tool built using Streamlit + Selenium that scrapes business information from **Google Maps**. It filters, scores, and extracts verified data like business name, address, map URL, and email — all in one click.

Ideal for sales teams, marketers, and startup growth hackers who need hyperlocal leads — fast.

---

## 🌟 Features

- 🗺️ Scrapes businesses directly from Google Maps based on keyword & location
- 📬 Enriches with email addresses via intelligent web crawling
- 🧠 Scores leads using simple heuristics
- 📊 Interactive filters, sort options, and visual metrics
- 🎨 Clean UI with sidebar, live progress, and download support
- 📁 One-click CSV export for CRM usage

---

## 🧠 Tech Stack

| Tool         | Purpose                          |
|--------------|-----------------------------------|
| `Streamlit`  | Interactive frontend              |
| `Selenium`   | Web automation for Google Maps    |
| `BeautifulSoup` | Email enrichment from websites |
| `Pandas`     | Data cleaning and export          |
| `Python`     | Core scripting logic              |

---

## 📸 UI Preview

![screenshot](https://imgur.com/a/4E3cW11.png) <!-- Replace with your actual screenshot URL -->

---

## 🛠 How It Works

1. Enter a **business keyword** (e.g., *Interior Designers*)  
2. Enter a **location** (e.g., *Hyderabad*)  
3. Click `🚀 Start Scraping`  
4. The app:
   - Loads Google Maps
   - Extracts top listings
   - Visits each business profile
   - Finds the business website
   - Crawls it for any email addresses
5. Scores and displays the results in a table
6. Export to CSV and plug into your CRM

---

## 💡 AI Intelligence Explained

While not using a neural network, this project uses:

- 🧠 **Rule-based automation** to smartly extract business profiles  
- 📬 **Pattern-matching enrichment** (for email discovery)  
- 📈 **Heuristic lead scoring** based on email presence  
- Optional: expandable with GPT tagging or classification

---

## 🚧 Folder Structure

