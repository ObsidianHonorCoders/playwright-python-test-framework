import pytest
from playwright.sync_api import Page, expect

from tests.data.quotes import MAXIMUM, MINIMUM
from tests.pages.transfer_page import TransferPage


@pytest.fixture
def transfer(page: Page, base_url: str):
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(15000)
    view = TransferPage(page)
    view.open(base_url)
    return view


def test_usd_mxn_quote_and_draft_confirmation(transfer):
    transfer.quote("100.00")
    transfer.assert_quote("1 USD = 17.00 MXN", "3.00 USD", "1700.00 MXN", "103.00 USD")
    transfer.create_draft()
    expect(transfer.page.get_by_test_id("confirmation")).to_contain_text("Draft created successfully. Reference: GS-")


@pytest.mark.parametrize(("amount", "message"), [
    ("", "Enter a transfer amount."),
    ("0", "Transfer amount must be greater than zero."),
    ("-1", "Enter a valid positive number."),
    ("abc", "Enter a valid positive number."),
    ("5000.01", "Maximum transfer amount is 5,000.00 USD."),
    ("0.50", "Minimum transfer amount is 1.00 USD."),
])
def test_invalid_amounts_show_validation_without_success(transfer, amount, message):
    transfer.quote(amount)
    expect(transfer.page.get_by_test_id("validation-error")).to_have_text(message)
    transfer.create_draft()
    expect(transfer.page.get_by_test_id("confirmation")).to_be_empty()
    transfer.assert_quote("—", "—", "—", "—")


def test_missing_required_currency_shows_validation(transfer):
    transfer.amount.fill("100")
    expect(transfer.page.get_by_test_id("validation-error")).to_have_text("Select both currencies.")
    transfer.create_draft()
    expect(transfer.page.get_by_test_id("confirmation")).to_be_empty()


def test_unsupported_pair_shows_validation(transfer):
    transfer.quote("100", destination="EUR")
    expect(transfer.page.get_by_test_id("validation-error")).to_have_text("This currency pair is not supported.")
    transfer.create_draft()
    expect(transfer.page.get_by_test_id("confirmation")).to_be_empty()


@pytest.mark.parametrize(("amount", "recipient", "total"), [
    (f"{MINIMUM:.2f}", "17.00 MXN", "4.00 USD"),
    (f"{MAXIMUM:.2f}", "85000.00 MXN", "5003.00 USD"),
    ("1.005", "17.09 MXN", "4.00 USD"),
])
def test_minimum_maximum_and_decimal_rounding(transfer, amount, recipient, total):
    transfer.quote(amount)
    transfer.assert_quote("1 USD = 17.00 MXN", "3.00 USD", recipient, total)


def test_multiple_quotes_update_results_in_one_session(transfer):
    transfer.quote("100")
    transfer.assert_quote("1 USD = 17.00 MXN", "3.00 USD", "1700.00 MXN", "103.00 USD")
    transfer.amount.fill("200")
    transfer.assert_quote("1 USD = 17.00 MXN", "3.00 USD", "3400.00 MXN", "203.00 USD")
