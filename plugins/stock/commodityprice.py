import os
from semantic_kernel.prompt_template import PromptTemplateConfig,InputVariable
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings


class rulesetPlugin:
    def __init__(self):
        self.current_folder_path = os.getcwd()

    async def define_function(self):
        # Add jinja2 plugins
        with open(f"{self.current_folder_path}/plugins/utils/analyze_commodity_price.jinja2", "r") as file:
            analyze_commodity_price = file.read()
            if analyze_commodity_price:
                # Add the stock function
                prompt_template_config_for_stockprice = PromptTemplateConfig(
                    template=analyze_commodity_price,
                    name="analyze_commodity_price",
                    description="Analyzes the commodity price for the contract negotiation. This is required to execute the negotation strategy.",
                    template_format="jinja2",
                    input_variables=[       
                        InputVariable(name="commodity_prices", description="historical and current commodity prices",
                                  is_required=True),                    
                    ],
                    execution_settings=AzureChatPromptExecutionSettings(
                        temperature=0.0),
                        response_format={"type": "text"},
                )
        return prompt_template_config_for_stockprice
    

    async def define_function(self):
        # Add jinja2 plugins
        with open(f"{self.current_folder_path}/plugins/utils/analyze_commodity_price.jinja2", "r") as file:
            analyze_market = file.read()
            if analyze_market:
                # Add the stock function
                prompt_template_config_for_analyzemarket = PromptTemplateConfig(
                    template=analyze_market,
                    name="analyze_market",
                    description="Analyzes the market for the contract negotiation. This is required to execute the negotation strategy.",
                    template_format="jinja2",
                    input_variables=[       
                        InputVariable(name="news", description="live and historical market news & sentiment data from a large & growing selection of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range of topics such as fiscal policy, mergers & acquisitions, IPOs, etc.",
                                  is_required=True),                    
                    ],
                    execution_settings=AzureChatPromptExecutionSettings(
                        temperature=0.0),
                        response_format={"type": "text"},
                )
        return prompt_template_config_for_analyzemarket