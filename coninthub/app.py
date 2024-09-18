import streamlit as st
import datetime
import sys
import pandas as pd

from coninthub.contract_meta_manager.contractMetadata import ContractMetadata
from coninthub.negotiation_monitor.main import calc_renewal_time

def main():
    st.title("Contractual Intelligence Hub")

     # Create tabs
    tabs = st.tabs(["Market Overview", "Suppliers", "Playbooks", "Contract Monitor", "Negotiation Strategist"])
    
    with tabs[0]:
       display_market_overview()

    with tabs[1]:
       display_supplier_overview()

    with tabs[2]:
        display_playbooks()
    
    with tabs[3]:
        display_contract_monitor()

    with tabs[4]:
        display_negotiation_strategist()

def display_playbooks():
    st.header("Renewal Playbook")
    
    # Read the content of the renewal.jinja2 file
    try:
        with open('plugins/utils/renewal.jinja2', 'r') as file:
            renewal_content = file.read()
    except FileNotFoundError:
        renewal_content = "File not found."

    # Display the content in a text box
    st.text_area("Renewal Playbook Content", renewal_content, height=600)

    st.header("Ruleset")

    # Read the content of the ruleset.jinja2 file
    try:
        with open('plugins/utils/ruleset.jinja2', 'r') as file:
            ruleset_content = file.read()
    except FileNotFoundError:
        ruleset_content = "File not found."

    # Display the content in a text box
    st.text_area("Ruleset Content", ruleset_content, height=300)
             
def display_supplier_overview():
    st.header("Suppliers")
    
    # Example data
    suppliers = [
        {"Company": "AluminiumY", "Location": "USA", "Contact": "contact@aluminiumy.com"},
        {"Company": "AluminiumX", "Location": "Canada", "Contact": "contact@aluminiumx.com"},
        {"Company": "Contoso1", "Location": "UK", "Contact": "contact@contoso1.com"},
        {"Company": "Contoso2", "Location": "Germany", "Contact": "contact@contoso2.com"},
    ]
    
    # Create a DataFrame for the table
    df_suppliers = pd.DataFrame(suppliers)
    
    # Display the table
    st.table(df_suppliers)


def display_negotiation_strategist():
    st.header("Negotiation Strategist")
    st.write("Content for Negotiation Strategist goes here.")

def display_market_overview():
    st.header("Commodity Prices")
    
    # Example data for market prices
    market_data = [
        {"Commodity": "Aluminium", "Current Price": "$2,500", "Change Last Month": "+2%", "Change Last Year": "+10%"}
    ]
    
    # Create a DataFrame for the table
    df_market = pd.DataFrame(market_data)
    
    # Display the table without the index
    st.table(df_market.style.hide(axis='index'))
    
def display_contract_monitor():

        # Example data
    contracts = [
        ContractMetadata(
            agreementCode="AG001",
            agreementName="Supply Agreement 1",
            supplierId="SUP001",
            supplierName="AluminiumY",
            contractValue=15000000,
            startDate=datetime.datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
            expiryDate=datetime.datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            contractExpiryDateInMonth=12,
            supplierCriticality="Tier 1 - Business Critical",
            FinancialRiskScore="High",
            AutoRenewal="No",
            priceProtectionClause="partial - medium risk",
            businessUnit="R&D",
            singleSource="Yes however high transition costs assumed",
            terminationForConvenienceClause="yes w/6 month notice",
            lastSourcing="high risk",
            commodityCode="COM001",
            commodityDesc="Aluminium",
            status="Active"
        )
    ]

     # Create a list of dictionaries for the table
    table_data = [
        {
            "Supplier Name": contract.supplierName,
            "Commodity": contract.commodityDesc,
            "Contract Value": contract.contractValue,
            "Contract Expiry Date": contract.expiryDate
        }
        for contract in contracts
    ]

    st.table(table_data)

    if st.button('Run Evaluation'):
        renewal = calc_renewal_time()
        st.text_area("Renewal Information", renewal)




if __name__ == "__main__":
    main()