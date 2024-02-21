from flask_restful import Resource, abort

from bloackaid.logger import logger
from bloackaid.resource.utils import check_if_address_is_valid_or_abort
from bloackaid.web3_handler.approval_handler import ApprovalHandler, FailedGettingApprovals


class ApprovalsApi(Resource):
    def get(self, address: str):
        check_if_address_is_valid_or_abort(address)
        try:
            approval_events: list[str] = ApprovalHandler(address).get_approval_events()
            return approval_events, 200
        except Exception as e:
            message: str = f'Failed getting approvals for address {address}, Exception: {e}'
            logger.exception(message)
            abort(500, error=message)
