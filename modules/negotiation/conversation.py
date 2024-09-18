from semantic_kernel.functions.kernel_function_decorator import kernel_function
import json
import logging

class NegotiationConversation:
    def __init__(self):
        self.logger = logging.getLogger("kernel")

    @kernel_function(
            name="get_contract_metadata",
            description="Get the contract metadata by agreementCode",
    )
    async def get_contract_metadata_by_agreementCode(self,agreementCode: str)-> dict:
        """
        Get the contract metadata from the user by AgreementCode
        """
        self.logger.info(f"Getting contract metadata for agreementCode {agreementCode}")
        with open("plugins/utils/contract_metadata.json", "r") as file:
            contract_list = json.loads(file.read())

        for contract in contract_list:
            if contract["agreementCode"] == agreementCode:
                self.logger.info(f"Found contract metadata {contract}")
                return contract