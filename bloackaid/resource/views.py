from bloackaid.resource import api
from bloackaid.resource.approvals import ApprovalsApi
from bloackaid.resource.index import IndexApi

api.add_resource(ApprovalsApi, '/approvals/<string:address>', strict_slashes=False)
api.add_resource(IndexApi, '/', strict_slashes=False)
