import requests

def currency_rates():
    privat_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    privat_data = requests.get(privat_url).json()

    mono_url = 'https://api.monobank.ua/bank/currency'
    mono_data = requests.get(mono_url).json()

    privat_rates = {}
    for item in privat_data:
        ccy = item.get('ccy')
        if ccy in ['USD', 'EUR']:
            privat_rates[ccy] = {
                'sale': float(item['sale']),
                'buy': float(item['buy'])
            }

    mono_rates = {'USD': {'sale': 0.0, 'buy': 0.0}, 'EUR': {'sale': 0.0, 'buy': 0.0}}

    if isinstance(mono_data, list):
        for item in mono_data:
            if item.get('currencyCodeB') == 980:
                if item.get('currencyCodeA') == 840:
                    mono_rates['USD']['rateCross'] = item.get('rateCross')
                    mono_rates['USD']['sale'] = item.get('rateSell', item.get('rateCross'))
                    mono_rates['USD']['buy'] = item.get('rateBuy', item.get('rateCross'))
                elif item.get('currencyCodeA') == 978:
                    mono_rates['EUR']['rateCross'] = item.get('rateCross')
                    mono_rates['EUR']['sale'] = item.get('rateSell', item.get('rateCross'))
                    mono_rates['EUR']['buy'] = item.get('rateBuy', item.get('rateCross'))

    line = "-" * 74
    print(line)
    print(f"| {'':<18} | {'PRIVAT':<20} | {'MONOBANK':<24} |")
    print(line)

    usd_p_sale = f"{privat_rates.get('USD', {}).get('sale', 0.0):.4f}"
    usd_m_sale = f"{mono_rates['USD']['sale']:.4f}"
    print(f"| {'DOLL USA':<9} {'sale':<8} | {usd_p_sale:<20} | {usd_m_sale:<24} |")

    usd_p_buy = f"{privat_rates.get('USD', {}).get('buy', 0.0):.4f}"
    usd_m_buy = f"{mono_rates['USD']['buy']:.4f}"
    print(f"| {'DOLL USA':<9} {'buy':<8} | {usd_p_buy:<20} | {usd_m_buy:<24} |")

    eur_p_sale = f"{privat_rates.get('EUR', {}).get('sale', 0.0):.4f}"
    eur_m_sale = f"{mono_rates['EUR']['sale']:.4f}"
    print(f"| {'EURO':<9} {'sale':<8} | {eur_p_sale:<20} | {eur_m_sale:<24} |")

    eur_p_buy = f"{privat_rates.get('EUR', {}).get('buy', 0.0):.4f}"
    eur_m_buy = f"{mono_rates['EUR']['buy']:.4f}"
    print(f"| {'EURO':<9} {'buy':<8} | {eur_p_buy:<20} | {eur_m_buy:<24} |")

    print(line)


if __name__ == "__main__":
    currency_rates()
