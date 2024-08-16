* ======================================================================
* Paper  : Global Real Interest Rate Dynamics and Monetary Policy Announcements
* Author : Alper Yıldırım
* Date   : August 2024
*
* This program includes relevant commands to reproduce the analysis in the paper.
*
* Database used: 
*
* ======================================================================

* Install required packages, if not already installed
ssc install ranktest
ssc install ivreg2
ssc install ftools
ssc install estout

* To read data, change the global path
global PROJECT_DIR "C:/Users/yildi/OneDrive/Desktop/Personal OneDrive/yildirim-masters-thesis/processed_data/master_data"

* ======================================================================
* 1. Germany
* ======================================================================
import delimited "$PROJECT_DIR/german_master.csv"

* Create the interaction terms manually
gen interaction = spread * infed3dwindow
gen instrumented_interaction = vix * infed3dwindow

* Main Specification
ivreg2 yrchange (spread interaction = vix instrumented_interaction) infed3dwindow dxy, robust

* Since instrument is weak, add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lagw = (L1.spread + L2.spread + L3.spread + L4.spread + L5.spread) / 5

ivreg2 yrchange (spread interaction = vix instrumented_interaction spread_lag1w) infed3dwindow dxy, robust

*** FROM RM IN FINANCIAL ECONOMICS ***
*eststo w270: reghdfe loan_change_to_assets c.shock_270##c.ccyb_rate fiscal_sti_tril bond_yield esi gdp_growth, absorb(bank date) vce(cluster country)
*quietly estadd local fixedm "Yes", replace
*quietly estadd local fixedy "Yes", replace
*quietly estadd local days "270", replace
* esttab w60 w90 w120 w180 w270 using "sample_reg.tex", replace label se star(* 0.10 ** 0.05 *** 0.01) s(days fixedm fixedy r2 N,label("Initial Shock Window"  "Bank FE" "Time FE" "R^2" "Observations"))

* ======================================================================
* 2. United Kingdom
* ======================================================================
import delimited "$PROJECT_DIR/uk_master.csv"

* ======================================================================
* 3. Japan
* ======================================================================
import delimited "$PROJECT_DIR/japan_master.csv"

* ======================================================================
* 4. Canada
* ======================================================================
import delimited "$PROJECT_DIR/canada_master.csv"

* ======================================================================
* 5. Switzerland
* ======================================================================
import delimited "$PROJECT_DIR/swiss_master.csv"

* ======================================================================
* 6. Australia
* ======================================================================
import delimited "$PROJECT_DIR/australia_master.csv"
