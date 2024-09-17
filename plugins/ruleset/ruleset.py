import os
from semantic_kernel.prompt_template import PromptTemplateConfig
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings


class rulesetPlugin:
    def __init__(self):
        self.current_folder_path = os.getcwd()

    async def define_function(self):
        # Add jinja2 plugins
        with open(f"{self.current_folder_path}/plugins/utils/ruleset.jinja2", "r") as file:
            rulesets = file.read()
            if rulesets:
                # Add the ruleset function
                prompt_template_config_for_ruleset = PromptTemplateConfig(
                    template=rulesets,
                    name="ruleset",
                    description="defines the ruleset for the contract negotiation. This is required to execute the negotation strategy.",
                    template_format="jinja2",
                    input_variables=[                            
                    ],
                    execution_settings=AzureChatPromptExecutionSettings(
                        temperature=0.0),
                )
        return prompt_template_config_for_ruleset