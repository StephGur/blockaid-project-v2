from flask import abort


def check_if_address_is_valid_or_abort(address: str):
    try:
        int(address, 16)
    except ValueError:
        abort(400, error=f'The provided address {address} is not a valid hash')
