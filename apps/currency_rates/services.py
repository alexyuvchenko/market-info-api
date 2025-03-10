"""Services for fetching currency and Bitcoin rates."""

import datetime

from .clients import BlockchainApiClient, EcbApiClient


def get_bitcoin_price_eur():
    """
    Get the current Bitcoin price in EUR from Blockchain.com API.

    This function fetches the 15min delayed Bitcoin market price in EUR
    from the Blockchain.com ticker API.

    Returns:
        float: Bitcoin price in EUR or None if there was an error
    """
    client = BlockchainApiClient()
    return client.get_bitcoin_price_eur()


def get_last_month_date_range():
    """
    Returns:
        dict: A dictionary with 'start_date' and 'end_date' keys as strings in YYYY-MM-DD format
    """
    today = datetime.date.today()
    # Get the first day of the current month
    first_day_current_month = today.replace(day=1)
    # Get the last day of the previous month
    last_day_previous_month = first_day_current_month - datetime.timedelta(days=1)
    # Get the first day of the previous month
    first_day_previous_month = last_day_previous_month.replace(day=1)

    return {
        "start_date": first_day_previous_month.strftime("%Y-%m-%d"),
        "end_date": last_day_previous_month.strftime("%Y-%m-%d"),
    }


def get_eur_to_gbp_rate(date_range=None):
    """
    Get the monthly EUR to GBP conversion rate from the European Central Bank API.

    This function fetches the monthly average conversion rate for the last month.

    Returns:
        float: EUR to GBP conversion rate or None if there was an error
    """
    client = EcbApiClient()

    return client.get_eur_to_gbp_rate(date_range)


def calculate_bitcoin_price_gbp(bitcoin_eur, eur_to_gbp):
    """
    Calculate the Bitcoin price in GBP using the EUR price and EUR to GBP conversion rate.

    Args:
        bitcoin_eur (float): Bitcoin price in EUR
        eur_to_gbp (float): EUR to GBP conversion rate

    Returns:
        float: Bitcoin price in GBP or None if any input is None
    """
    if bitcoin_eur is None or eur_to_gbp is None:
        return None

    return bitcoin_eur / eur_to_gbp


def get_currency_rates():
    """
    Get all currency rates in a single function.

    This function fetches:
    1. Bitcoin price in EUR
    2. EUR to GBP conversion rate
    3. Bitcoin price in GBP (calculated)

    Returns:
        dict: Dictionary containing all currency rates
    """
    # Get Bitcoin price in EUR
    bitcoin_eur = get_bitcoin_price_eur()

    # Get EUR to GBP conversion rate
    date_range_month = get_last_month_date_range()
    eur_to_gbp_last_month = get_eur_to_gbp_rate(date_range_month)
    eur_to_gbp_today = get_eur_to_gbp_rate()

    # Calculate Bitcoin price in GBP
    bitcoin_gbp = calculate_bitcoin_price_gbp(bitcoin_eur, eur_to_gbp_today)

    return {
        "bitcoin_eur": bitcoin_eur,
        "eur_to_gbp": eur_to_gbp_last_month,
        "bitcoin_gbp": bitcoin_gbp,
    }
