class InvalidBlock(Exception):
    pass


class KeysExist(Exception):
    pass


class InvalidTransaction(Exception):
    pass


class InvalidBlockchain(Exception):
    pass


class WorseBlockchain(Exception):
    pass


class NotEnoughTransactions(Exception):
    msg = "Not enought transactions to build a block."


class UnsuccessfulPatch(Exception):
    pass
