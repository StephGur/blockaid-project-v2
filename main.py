from web3 import Web3
from web3._utils.filters import Filter
from web3.types import LogReceipt

from bloackaid.consts import ABI
from config import BLOCKAID_CONFIG

w3 = Web3(Web3.HTTPProvider(BLOCKAID_CONFIG.INFURA_URL))


class FailedGettingApprovals(Exception):
    pass


class Approvals():
    CHUNK_SIZE: int = 1000000

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
                approvals.extend(self._get_approval_chunk(to_block, from_block))
                to_block = to_block - self.CHUNK_SIZE
                from_block = from_block - self.CHUNK_SIZE

            return approvals
        except FailedGettingApprovals as e:
            raise FailedGettingApprovals(f'Failed getting approvals') from e

    def _get_approval_chunk(self, to_block, from_block):
        try:
            # Filter for Approval events involving the given address
            filter_approval: Filter = w3.eth.filter({
                "fromBlock": from_block,
                "toBlock": to_block,
                "address": self.address,
                "topics": [self.event_signature]
            })

            # Get all Approval events
            approval_events: list[LogReceipt] = w3.eth.get_filter_logs(filter_approval.filter_id)
            return self._parse_approvals_response(approval_events)
        except Exception as e:
            raise FailedGettingApprovals(f'Failed getting approvals') from e

    def _parse_approvals_response(self, approval_events: list[LogReceipt]) -> list[str]:
        return [self._parse_single_response(event) for event in approval_events]

    def _parse_single_response(self, event: LogReceipt) -> str:
        from_address = w3.to_checksum_address(event['topics'][1].hex()[26:])
        to_address = w3.to_checksum_address(event['topics'][2].hex()[26:])
        from_address_v2 = w3.to_hex(event['topics'][1])
        to_address_v2 = w3.to_hex(event['topics'][2])
        value = int(event['data'].hex(), 16)
        value = w3.from_wei(event["data"], 'ether')
        return f"From: {from_address} To: {to_address} with Value: {value}"


def get_approvals(address):
    # ERC-20 Approval event signature
    event_signature = w3.keccak(text="Approval(address,address,uint256)").hex()

    bla = w3.eth.filter('latest').get_all_entries()
    print(bla)

    # Filter for Approval events involving the given address
    filter_approval: Filter = w3.eth.filter({
        "fromBlock": "earliest",
        "toBlock": "latest",
        "address": address,
        "topics": [event_signature]
    })

    # Get all Approval events
    approval_events = w3.eth.get_filter_logs(filter_approval.filter_id)

    latest_block = w3.eth.block_number
    from_block = latest_block - 1000

    filter_params = {
        "fromBlock": from_block,
        "toBlock": "latest",
        "address": address,
        "topics": [event_signature]
    }

    approval_events2 = w3.eth.get_logs(filter_params)

    weth_contract = w3.eth.contract(address=address, abi=ABI)

    # fetch transfer events in the last block
    logs = weth_contract.events.Approval().get_logs(fromBlock=w3.eth.block_number)

    # Print the details of each Approval event
    events: list[str] = []

    for event in approval_events:
        from_address = w3.to_checksum_address(event['topics'][1].hex()[26:])
        to_address = w3.to_checksum_address(event['topics'][2].hex()[26:])

        from_address_v2 = w3.to_hex(event['topics'][1])
        to_address_v2 = w3.to_hex(event['topics'][2])

        value = int(event['data'].hex(), 16)
        value = w3.from_wei(event["data"], 'ether')
        print(f"From: {from_address} To: {to_address} with Value: {value}")
        events.append(f"From: {from_address} To: {to_address} with Value: {value}")

def parse_approvals_response(approval_events) -> list[str]:
    events: list[str] = []

    for event in approval_events:
        from_address = w3.to_checksum_address(event['topics'][1].hex()[26:])
        to_address = w3.to_checksum_address(event['topics'][2].hex()[26:])

        from_address_v2 = w3.to_hex(event['topics'][1])
        to_address_v2 = w3.to_hex(event['topics'][2])

        value = int(event['data'].hex(), 16)
        value = w3.from_wei(event["data"], 'ether')
        events.append(f"From: {from_address} To: {to_address} with Value: {value}")


if __name__ == "__main__":
    # Replace 'YOUR_PUBLIC_ADDRESS' with the actual public address you want to investigate
    # target_address = '0x005e20fCf757B55D6E27dEA9BA4f90C0B03ef852'
    target_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

    get_approvals(target_address)
