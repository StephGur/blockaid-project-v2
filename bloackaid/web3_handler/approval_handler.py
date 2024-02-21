from web3.types import LogReceipt

from bloackaid.web3_handler import w3


class FailedGettingApprovals(Exception):
    pass


class ApprovalHandler():
    CHUNK_SIZE = 100000

    def __init__(self, address: str):
        self.address = address
        self.event_signature = w3.keccak(text="Approval(address,address,uint256)").hex()

    def get_approval_events(self) -> list[str]:
        approvals = []
        latest_block = w3.eth.block_number

        from_block = latest_block - self.CHUNK_SIZE
        to_block = latest_block

        try:
            while from_block >= 0:
                #0x116E1AB, #0x11717E5
                approvals.extend(self._get_approval_chunk('0x116E1AB', '0x11717E5'))
                to_block = to_block - self.CHUNK_SIZE
                from_block = from_block - self.CHUNK_SIZE

            return approvals
        except Exception as e:
            raise Exception

    def _get_approval_chunk(self, from_block, to_block):
        try:
            # Filter for Approval events involving the given address
            filter_approval = w3.eth.filter({
                "fromBlock": from_block,
                "toBlock": to_block,
                "address": self.address,
                "topics": [self.event_signature]
            })

            # Get all Approval events
            approval_events: list[LogReceipt] = w3.eth.get_filter_logs(filter_approval.filter_id)
            return self._parse_approvals_response(approval_events)
        except Exception as e:
            raise Exception

    def _parse_approvals_response(self, approval_events: list[LogReceipt]) -> list[str]:
        return [self._parse_single_response(event) for event in approval_events]

    def _parse_single_response(self, event: LogReceipt) -> str:
        from_address = w3.to_checksum_address(event['topics'][1].hex()[26:])
        to_address = w3.to_checksum_address(event['topics'][2].hex()[26:])
        value = int(event['data'].hex(), 16)
        token_contract_address = w3.to_checksum_address(event['address'])
        token_symbol = self._get_token_symbol(token_contract_address)
        return f"Approval on: {token_symbol}  on amount of {value}"

    def _get_token_symbol(self, token_contract_address):
        try:
            contract = w3.eth.contract(address=token_contract_address, abi=[])
            token_symbol = contract.functions.symbol().call()
            return token_symbol
        except Exception as e:
            return "Unknown"
