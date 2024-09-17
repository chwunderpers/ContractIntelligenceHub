from dataclasses import dataclass
from datetime import date

@dataclass
class ContractMetadata:
    agreementCode: str
    agreementName: str
    supplierId: str
    supplierName: str
    contractValue: int
    startDate: date
    expiryDate: date
    contractExpiryDateInMonth: int
    supplierCriticality: str
    FinancialRiskScore: str
    AutoRenewal: str
    priceProtectionClause: str
    businessUnit: str
    singleSource: str
    terminationForConvenienceClause: str
    lastSourcing: str
    commodityCode: str
    commodityDesc: str
    status: str