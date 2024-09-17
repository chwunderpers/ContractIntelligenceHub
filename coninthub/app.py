import streamlit as st
import datetime
import sys

from coninthub.contract_meta_manager.contractMetadata import ContractMetadata

def main():
    st.title("Contractual Intelligence Hub")

     # Create tabs
    tabs = st.tabs(["Market Signals", "Contract Monitor", "Negotiation Strategist"])
    
    with tabs[0]:
        st.header("Market Signals")
        st.write("Content for Market Signals goes here.")

    with tabs[1]:
        display_contract_monitor()
    
    with tabs[2]:
        st.header("Negotiation Strategist")
        st.write("Content for Negotiation Strategist goes here.")
    
    
def display_contract_monitor():
    st.header("Upcoming Contract Renewals")

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


if __name__ == "__main__":
    main()