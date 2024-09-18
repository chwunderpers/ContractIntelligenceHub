import asyncio
import logging

import os
import datetime

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior, FunctionChoiceType
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

from plugins import configure_services
from modules.negotiation.conversation import NegotiationConversation
from modules.stock.alphaVantagePlugin import AlphaVantagePlugin
from coninthub.contract_meta_manager.contractManager import ContractManager
from coninthub.playbook_manager.playbookManager import get_playbook

async def calc_renewal_time(agreementCode: str):
    print(f"Calculating renewal time for agreement code: {agreementCode}")
    currentDateTime = datetime.datetime.now(
            datetime.UTC).strftime('%Y-%m-%d')
    
    # Initialize the kernel and other classes
    kernel = Kernel()
    configService = configure_services.configurationService(kernel)
    await configService.configure_services()
    negotiationService = NegotiationConversation()
    alphaVantageService = AlphaVantagePlugin(os.getenv("ALPHA_VANTAGE_KEY"))
    kernel.add_plugin(alphaVantageService, "alphaVantageService")
    kernel.add_plugin(negotiationService, "negotationService")
    
    

    # Add Azure OpenAI chat completion
    kernel.add_service(AzureChatCompletion(
        deployment_name="gpt-4o",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    ))

    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("kernel").setLevel(logging.INFO)

    chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(
            max_tokens=1000,
            temperature=0.0,
            top_p=0.8,
            response_format={"type": "json_object"},
            function_choice_behavior=FunctionChoiceBehavior(type=FunctionChoiceType.AUTO,
                maximum_auto_invoke_attempts=5,  
                filters={"excluded_plugins": ["NegotationMonitorPlugin" ], "excluded_functions": [ "UtilsPlugin-NegotiationStretegy"]},
            )
    )      

     # Define input variables as a dictionary
    input_variables = [
        InputVariable(name="currentDateTime", description="current date", is_required=True),
        InputVariable(name="agreementCode", type="agreement Code of the contract", is_required=True),
    ]

    with open("plugins/utils/negotiation_monitor.jinja2", "r") as file:
        negotiation_monitor = file.read()
        if negotiation_monitor:
            # Add the renewal function
            prompt_template_config_for_negotiation = PromptTemplateConfig(
                template=negotiation_monitor,
                name="calcRenewalTime",
                description="calculate renewal time based on the agreement code.",
                template_format="jinja2",
                input_variables=input_variables,
                execution_settings=AzureChatPromptExecutionSettings(
                    temperature=0.0),
            )
    negotationMonitorConfiguration = prompt_template_config_for_negotiation

    kernel.add_function(
            function_name="calcRenewalTime",
            plugin_name="NegotationMonitorPlugin",
            prompt_template_config=negotationMonitorConfiguration,
            template_format="jinja2",
        )

    arguments = KernelArguments(settings=execution_settings)
    arguments["agreementCode"] = agreementCode
    arguments["currentDateTime"] = currentDateTime

    result = await kernel.invoke(settings=execution_settings, arguments=arguments, 
                                 plugin_name="NegotationMonitorPlugin", function_name="calcRenewalTime")
    
    # Print the results
    print("Result > " + str(result))

    return result