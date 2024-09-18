import json
import logging
import streamlit as st
import datetime
import sys
import pandas as pd
import dotenv

from coninthub.contract_meta_manager.contractMetadata import ContractMetadata
from coninthub.negotiation_monitor.main import calc_renewal_time
from opentelemetry.sdk._logs.export import ConsoleLogExporter, BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry._logs import set_logger_provider

import asyncio

def main():
    st.title("Contractual Intelligence Hub")

     # Create tabs
    tabs = st.tabs(["Market Overview", "Suppliers", "Playbooks", "Contracts", "Contract Monitor", "Negotiation Strategist"])
    
    with tabs[0]:
       display_market_overview()

    with tabs[1]:
       display_supplier_overview()

    with tabs[2]:
        display_playbooks()
    
    with tabs[3]:
        display_contracts()
    
    with tabs[4]:
        display_contract_monitor()

    with tabs[5]:
        display_negotiation_strategist()

def display_contracts():
    try:
        with open('plugins/utils/contract_metadata.json', 'r') as file:
            contract_metadata_content = file.read()
    except FileNotFoundError:
        contract_metadata_content = "File not found."

    # Display the content in a text box
    st.text_area("Contract Metadata", contract_metadata_content, height=600)
    
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

    # Create an empty DataFrame with the specified columns
    if 'df_contract_monitor' not in st.session_state:
        columns = ["Agreement Code", "Supplier Name", "Commodity", "Suggested Start of Renewal", "Reasoning"]
        st.session_state.df_contract_monitor = pd.DataFrame(columns=columns)

    if st.button('Run Evaluation'):

        async def run_evaluation():
            try:
                renewal = await calc_renewal_time("AG001")
                renewal_json = json.loads(str(renewal)) # Convert to JSON
                new_row = pd.DataFrame([{
                    "Agreement Code": "AG001",
                    "Supplier Name": "AluminiumY",
                    "Commodity": "Aluminium",
                    "Suggested Start of Renewal": renewal_json["timeframe"],
                    "Reasoning": renewal_json["reasoning"]
                }])
                st.session_state.df_contract_monitor = pd.concat([st.session_state.df_contract_monitor, new_row], ignore_index=True)
            except Exception as e:
                st.text_area("Error", str(e))

        result = asyncio.run(run_evaluation())

        st.table(st.session_state.df_contract_monitor.style.hide(axis='index'))

def set_up_logging():
    class KernelFilter(logging.Filter):
        """A filter to not process records from semantic_kernel."""

        # These are the namespaces that we want to exclude from logging for the purposes of this demo.
        namespaces_to_exclude: list[str] = [
            "semantic_kernel.functions.kernel_plugin",
            "semantic_kernel.prompt_template.kernel_prompt_template",
        ]

        def filter(self, record):
            return not any([record.name.startswith(namespace) for namespace in self.namespaces_to_exclude])

    resource = Resource.create({ResourceAttributes.SERVICE_NAME: "TelemetryExample"})

    exporters = []
    exporters.append(ConsoleLogExporter())

    # Create and set a global logger provider for the application.
    logger_provider = LoggerProvider(resource=resource)
    # Log processors are initialized with an exporter which is responsible
    # for sending the telemetry data to a particular backend.
    for log_exporter in exporters:
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    # Sets the global default logger provider
    set_logger_provider(logger_provider)

    # Create a logging handler to write logging records, in OTLP format, to the exporter.
    handler = LoggingHandler()
    # Add filters to the handler to only process records from semantic_kernel.
    handler.addFilter(logging.Filter("semantic_kernel"))
    handler.addFilter(KernelFilter())
    # Attach the handler to the root logger. `getLogger()` with no arguments returns the root logger.
    # Events from all child loggers will be processed by this handler.
    logger = logging.getLogger()
    logger.addHandler(handler)
    # Set the logging level to NOTSET to allow all records to be processed by the handler.
    logger.setLevel(logging.NOTSET)
    
if __name__ == "__main__":
    #load environment variables
    dotenv.load_dotenv(override=True)
    # set_up_logging()

    main()