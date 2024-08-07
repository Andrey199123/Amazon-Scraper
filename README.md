# Amazon Product Scraper and Analyzer

## Overview

This project consists of three main components: a web scraper, a data parser, and a data analyzer. The web scraper collects product data including title, price, url, review rating, and review count from Amazon's bestsellers list and saves that to a json file called products_[currentDate]. The parser processes and corrects data, and the analyzer compares data between different scraping sessions to identify changes in price, rating, and number of ratings, and computes averages. I have provided a few sample files that have already been collected for reference.

## Files

### 1. `index.js`

This file contains the web scraper that uses Puppeteer to collect product data from Amazon's bestsellers list.

### 2. `parser.py`

This file processes and corrects product data collected by the scraper. Sometimes puppeteer can collect null values and they get corrected if they were collected properly from any previous values from files. It also removes unwanted characters from titles, and synchronizes data between different JSON files.

### 3. `analyzer.py`

This file analyzes and compares product data between different scraping sessions. It identifies unique products in each file, computes averages for prices, ratings, and reviews, and compares these metrics between files, which is very useful to track how the market is trending. 

## Setup

### Prerequisites

- Node.js and npm
- Python 3.x
- Puppeteer and puppeteer-extra
- Required Python packages: `json`, `sys`, `glob`, `os`, `re`

### Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. Install Node.js dependencies:
    ```bash
    npm install puppeteer-extra puppeteer-extra-plugin-stealth
    ```

3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Update the executable path for Chrome in `index.js`:
    ```javascript
    const browser = await puppeteerExtra.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', // Add your browser's executable path here
    });
    ```

2. Update the Amazon bestsellers URL in `index.js`:
    ```javascript
    await page.goto('https://www.amazon.fr/gp/bestsellers'); // Add your Amazon bestseller's list link here
    ```

## Usage

### Running the Scraper

To run the web scraper and collect product data:
```bash
node .
```

### Running the parser
```
python parser.py
```

### Running the analyzer
```
python analyzer.py <file1.json> <file2.json>
```
