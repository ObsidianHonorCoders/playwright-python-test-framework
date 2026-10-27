from playwright.sync_api import Page, expect


class TransferPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.source = page.get_by_test_id("source-currency")
        self.destination = page.get_by_test_id("destination-currency")
        self.amount = page.get_by_test_id("amount")

    def open(self, base_url: str) -> None:
        self.page.goto(base_url)

    def quote(self, amount: str, source: str = "USD", destination: str = "MXN") -> None:
        self.source.select_option(source)
        self.destination.select_option(destination)
        self.amount.fill(amount)

    def create_draft(self) -> None:
        self.page.get_by_test_id("create-draft").click()

    def assert_quote(self, rate: str, fee: str, recipient: str, total: str) -> None:
        expect(self.page.get_by_test_id("exchange-rate")).to_have_text(rate)
        expect(self.page.get_by_test_id("fee")).to_have_text(fee)
        expect(self.page.get_by_test_id("recipient-amount")).to_have_text(recipient)
        expect(self.page.get_by_test_id("total-charged")).to_have_text(total)
