import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta

class CurrencyExchange:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    @staticmethod
    async def fetch_exchange_rates(date):
        async with aiohttp.ClientSession() as session:
            params = {"json": "", "date": date.strftime("%d.%m.%Y")}
            async with session.get(CurrencyExchange.API_URL, params=params, ssl=False) as response:
                data = await response.json()
                exchange_rates = {}
                for rate in data['exchangeRate']:
                    if rate['currency'] in ['EUR', 'USD']:
                        exchange_rates[rate['currency']] = {
                            'sale': rate['saleRate'],
                            'purchase': rate['purchaseRate']
                        }
                return exchange_rates

async def get_exchange_rates_for_last_n_days(num_days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days)

    exchange_data = []

    current_date = start_date
    while current_date <= end_date:
        exchange_rate = await CurrencyExchange.fetch_exchange_rates(current_date)
        exchange_data.append({current_date.strftime("%d.%m.%Y"): exchange_rate})
        current_date += timedelta(days=1)

    return exchange_data

async def main():
    parser = argparse.ArgumentParser(description="Get currency exchange rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days to retrieve exchange rates for.")
    args = parser.parse_args()

    if args.days > 10:
        print("Error: Cannot retrieve exchange rates for more than 10 days.")
        return

    exchange_rates = await get_exchange_rates_for_last_n_days(args.days)
    print(exchange_rates)

if __name__ == "__main__":
    asyncio.run(main())
