* ======================================================================
* Paper  : Global Real Interest Rate Dynamics and Monetary Policy Announcements
* Author : Alper Yıldırım
* Date   : September 2024
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
import delimited "$PROJECT_DIR/master_data.csv", clear

* ======================================================================
* 1. German Bunds
* ======================================================================

* Convert ECB decision dates to Boolean variable
gen inecb3dw = cond(inecb3dwindow == "True", 1, 0)

* Before moving into the IV approach, for statistical testing
regress change10yr spread if country == "DEU", robust
regress change10yr infed3dwindow if country == "DEU", robust
regress change10yr inecb3dw if country == "DEU", robust

regress change10yr spread infed3dwindow if country == "DEU", robust
regress change10yr spread inecb3dw if country == "DEU", robust
regress change10yr infed3dwindow inecb3dw if country == "DEU", robust

regress change10yr spread infed3dwindow inecb3dw if country == "DEU", robust
regress change10yr c.spread##i.infed3dwindow inecb3dw if country == "DEU", robust

* Add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lag1w = (L1_spread + L2_spread + L3_spread + L4_spread + L5_spread) / 5

eststo DE: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow) if country == "DEU", robust

* ======================================================================
* 2. United Kingdom
* ======================================================================

* Convert BoE decision dates to Boolean variable
gen inboe3dw = cond(inboe3dwindow == "True", 1, 0)

* Before moving into the IV approach, for statistical testing
regress change10yr spread if country == "GBP", robust
regress change10yr infed3dwindow if country == "GBP", robust
regress change10yr inboe3dw if country == "GBP", robust

regress change10yr spread infed3dwindow if country == "GBP", robust
regress change10yr spread inboe3dw if country == "GBP", robust
regress change10yr infed3dwindow inboe3dw if country == "GBP", robust

regress change10yr spread infed3dwindow inboe3dw if country == "GBP", robust
regress change10yr c.spread##i.infed3dwindow inboe3dw if country == "GBP", robust

* Add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lag1w = (L1_spread + L2_spread + L3_spread + L4_spread + L5_spread) / 5

eststo UK: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow) if country == "GBP", robust

* ======================================================================
* 3. Japan
* ======================================================================

* Convert BoJ decision dates to Boolean variable
gen inboj3dw = cond(inboj3dwindow == "True", 1, 0)

* Before moving into the IV approach, for statistical testing
regress change10yr spread, robust
regress change10yr infed3dwindow, robust
regress change10yr inboj3dw, robust

regress change10yr spread infed3dwindow, robust
regress change10yr spread inboj3dw, robust
regress change10yr infed3dwindow inboj3dw, robust

regress change10yr spread infed3dwindow inboj3dw, robust
regress change10yr c.spread##i.infed3dwindow inboj3dw, robust

* Add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lag1w = (L1_spread + L2_spread + L3_spread + L4_spread + L5_spread) / 5

eststo JP: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow), robust

* ======================================================================
* 4. Canada
* ======================================================================

* Convert BoC decision dates to Boolean variable
gen inboc3dw = cond(inboc3dwindow == "True", 1, 0)

* Before moving into the IV approach, for statistical testing
regress change10yr spread, robust
regress change10yr infed3dwindow, robust
regress change10yr inboc3dw, robust

regress change10yr spread infed3dwindow, robust
regress change10yr spread inboc3dw, robust
regress change10yr infed3dwindow inboc3dw, robust

regress change10yr spread infed3dwindow inboc3dw, robust
regress change10yr c.spread##i.infed3dwindow inboc3dw, robust

* Add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lag1w = (L1_spread + L2_spread + L3_spread + L4_spread + L5_spread) / 5

eststo CD: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow), robust

* ======================================================================
* 5. Switzerland
* ======================================================================

* Convert SNB decision dates to Boolean variable
gen insnb3dw = cond(insnb3dwindow == "True", 1, 0)

* Before moving into the IV approach, for statistical testing
regress change10yr spread, robust
regress change10yr infed3dwindow, robust
regress change10yr insnb3dw, robust

regress change10yr spread infed3dwindow, robust
regress change10yr spread insnb3dw, robust
regress change10yr infed3dwindow insnb3dw, robust

regress change10yr spread infed3dwindow insnb3dw, robust
regress change10yr c.spread##i.infed3dwindow insnb3dw, robust

* Add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lag1w = (L1_spread + L2_spread + L3_spread + L4_spread + L5_spread) / 5

eststo CH: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow), robust

* ======================================================================
* 6. Australia
* ======================================================================

* Convert RBA decision dates to Boolean variable
gen inrba3dw = cond(inrba3dwindow == "True", 1, 0)

* Before moving into the IV approach, for statistical testing
regress change10yr spread, robust
regress change10yr infed3dwindow, robust
regress change10yr inrba3dw, robust

regress change10yr spread infed3dwindow, robust
regress change10yr spread inrba3dw, robust
regress change10yr infed3dwindow inrba3dw, robust

regress change10yr spread infed3dwindow inrba3dw, robust
regress change10yr c.spread##i.infed3dwindow inrba3dw, robust

* Add lagged value of FX frictions as instrument
gen datevar = date(date, "YMD")
format datevar %td
tsset datevar, daily
* Due to missing days bcs of trading days, manually define the lagged values
gen L1_spread = spread[_n-1] if datevar[_n-1] != .
gen L2_spread = spread[_n-2] if datevar[_n-2] != .
gen L3_spread = spread[_n-3] if datevar[_n-3] != .
gen L4_spread = spread[_n-4] if datevar[_n-4] != .
gen L5_spread = spread[_n-5] if datevar[_n-5] != .
gen spread_lag1w = (L1_spread + L2_spread + L3_spread + L4_spread + L5_spread) / 5

eststo AU: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow), robust

* =====================================================================

* esttab w60 w90 w120 w180 w270 using "sample_reg.tex", replace label se star(* 0.10 ** 0.05 *** 0.01) s(days fixedm fixedy r2 N,label("Initial Shock Window"  "Bank FE" "Time FE" "R^2" "Observations"))

eststo M1: regress change10yr infed3dwindow, robust beta
eststo M2: regress change10yr spread, robust beta
eststo M3: regress change10yr spread infed3dwindow, robust beta
eststo M4: regress change10yr c.spread##i.infed3dwindow, robust beta
eststo M5: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow), robust
esttab M1 M2 M3 M4 M5 using "outputs.tex", p label star(* 0.1 ** 0.05 *** 0.01) replace

eststo M1: regress change10yr infed3dwindow, robust beta
eststo M2: regress change10yr spread, robust beta
eststo M3: regress change10yr spread infed3dwindow, robust beta
eststo M4: regress change10yr c.spread##i.infed3dwindow, robust beta
eststo M5: ivreg2 change10yr infed3dwindow (spread c.spread#i.infed3dwindow = spread_lag1w c.spread_lag1w#i.infed3dwindow), robust
esttab M1 M2 M3 M4 M5 using "outputs_beta.tex", beta p star(* 0.1 ** 0.05 *** 0.01)  label replace


