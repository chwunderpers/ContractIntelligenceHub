from semantic_kernel.functions.kernel_function_decorator import kernel_function
import json
import logging

class ContractManager:
    def get_contract_metadata_by_agreementCode(self,agreementCode: str)-> dict:
        with open("../../plugins/utils/contract_metadata.json", "r") as file:
            contract_list = json.loads(file.read())

        for contract in contract_list:
            if contract["agreementCode"] == agreementCode:
                self.logger.info(f"Found contract metadata {contract}")
                return contract