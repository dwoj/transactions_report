from datetime import datetime
from typing import Optional
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

from helpers import convert_to_utc, make_card_info, convert_to_pln, sort_by_date

app = FastAPI()

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    PLN = "PLN"

class Operation(BaseModel):
    created_at: datetime = datetime.now()
    currency: Currency
    amount: int
    description: str

class PayByLink(Operation):
    bank: str

class DirectPay(Operation):
    iban: str

class Card(Operation):
    cardholder_name: str
    cardholder_surname: str
    card_number: int

class Transactions(BaseModel):
    pay_by_link: Optional[list[PayByLink]]
    dp: Optional[list[DirectPay]]
    card: Optional[list[Card]]

class ReportItem(BaseModel):
    date: datetime
    type: str
    payment_mean: str
    description: str
    amount: int
    currency: str
    amount_in_pln: int

@app.post("/report/", response_model=list[ReportItem])
async def create_report(transactions: Transactions):
    report = []
    for transaction in transactions:
        if (transaction[0] == "pay_by_link" and transaction[1] != None):
            for t in transaction[1]:
                report.append({
                    "date": convert_to_utc(t.created_at),
                    "type": "pay_by_link",
                    "payment_mean": t.bank ,
                    "description": t.description,
                    "currency": t.currency,
                    "amount": t.amount,
                    "amount_in_pln": convert_to_pln(t.currency, t.amount, t.created_at)
                })
        if (transaction[0] == "dp" and transaction[1] != None):
            for t in transaction[1]:
                report.append({
                    "date": convert_to_utc(t.created_at),
                    "type": "dp",
                    "payment_mean": t.iban,
                    "description": t.description,
                    "currency": t.currency,
                    "amount": t.amount,
                    "amount_in_pln": convert_to_pln(t.currency, t.amount, t.created_at)
                })
        if (transaction[0] == "card" and transaction[1] != None):
            for t in transaction[1]:
                report.append({
                    "date": convert_to_utc(t.created_at),
                    "type": "card",
                    "payment_mean": make_card_info(t.cardholder_name, t.cardholder_surname, t.card_number),
                    "description": t.description,
                    "currency": t.currency,
                    "amount": t.amount,
                    "amount_in_pln": convert_to_pln(t.currency, t.amount, t.created_at)
                })
    sorted_report = sort_by_date(report)
    return sorted_report
