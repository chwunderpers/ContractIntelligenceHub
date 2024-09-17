import os

from semantic_kernel.prompt_template import PromptTemplateConfig,InputVariable
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings


class negotiationPlugin:
    def __init__(self):
        self.current_folder_path = os.getcwd()
        

    async def define_function(self):
        # Add jinja2 plugins
        with open(f"{self.current_folder_path}/plugins/utils/renewal.jinja2", "r") as file:
            negotiation = file.read()
            if negotiation:
                # Add the renewal function
                prompt_template_config_for_negotiation = PromptTemplateConfig(
                    template=negotiation,
                    name="NegotiationStretegy",
                    description="Create a strategy for the negotation based on variables defined in the function.",
                    template_format="jinja2",
                    input_variables=[],
                    execution_settings=AzureChatPromptExecutionSettings(
                        temperature=0.0),
                )
        return prompt_template_config_for_negotiation
    
