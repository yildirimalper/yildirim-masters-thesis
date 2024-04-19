# Master's Thesis

This repository contains the source code and data for my master's thesis project. The project explores the relationship between global financial cycles, long-term government bond yields, and monetary policy decisions.

## Project Overview

*to be written*

### Repository Structure
```plain
├── src/
|   ├── data_visualization/
|   ├── fetch_data/
|   ├── handle_bond_data/
|   ├── hillenbrand_replication/
├── original_data/
|   ├── australian_bond_yields/
|   ├── boc_bond_yields/
|   ├── boe_gilt_yields/
|   ├── france_oat_yields/
|   ├── german_bund_yields/
|   ├── japanese_bond_yields/
|   ├── swiss_bond_yields/
|   ├── gurkaynak2007.xlsx
|   ├── gurkaynak2010.xls
├── processed_data/
|   ├── monetary_policy_dates/
|   ├── yield_data/
|   ├── hillenbrand_replication.csv
├── sandbox/
├── figures/
├── paper/
├── utils/
|   ├── time_windows.py
├── environment.yml
├── CITATION
├── report.pdf
├── README.md
```

## Setup and Installation

To clone this repository in your local machine,

```shell
git clone https://github.com/yildirimalper/yildirim-masters-thesis
```

After cloning repository, by using the `environment.yml` file, you can recreate the exact environment required for the project with:

```shell
conda env create -f environment.yml
conda activate masters_thesis
```

## Acknowledgments

I would like to thank Dr. Janko Heineken for their guidance and support throughout the project.