curl -s "http://www.financialstability.gov/impact/DataTables/fsTable/transaction.csv" | grep $1 | python tarp_process_financialstabilitydotgov.py