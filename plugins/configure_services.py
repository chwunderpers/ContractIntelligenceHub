import semantic_kernel as sk
import logging
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions import KernelArguments

from plugins.negotiation.negotiation import negotiationPlugin
from plugins.ruleset.ruleset import rulesetPlugin  


class configurationService:
    def __init__(self,kernel: sk.Kernel):
        self.negotiationPlugin = negotiationPlugin()
        self.rulesetPlugin = rulesetPlugin()
        self.kernel = kernel
        self.logger = logging.getLogger("kernel")

    async def configure_services(self):
        self.logger.info(f"Importing plugin negotation strategy")
        negotationConfiguration = await self.negotiationPlugin.define_function()
        self.kernel.add_function(
            function_name="NegotiationStretegy",
            plugin_name="UtilsPlugin",
            prompt_template_config=negotationConfiguration,
            template_format="jinja2",
        )
        self.logger.info(f"Added stretegy plugin to the kernel")

        self.logger.info(f"Importing ruleset Plugin")
        rulesetConfiguration = await self.negotiationPlugin.define_function()
        self.kernel.add_function(
            function_name="ruleset",
            plugin_name="UtilsPlugin",
            prompt_template_config=rulesetConfiguration,
            template_format="jinja2",
        )
        self.logger.info(f"Added ruleset plugin to the kernel")
        return self.kernel

    




