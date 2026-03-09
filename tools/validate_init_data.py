from urllib.parse import parse_qsl
from config.logger import logger
import hmac
from hashlib import sha256
import json


def validate_init_data(init_data: str, bot_token: str):
    data_dict = dict(parse_qsl(init_data))
    logger.info(data_dict)
    hash = data_dict.pop('hash')
    check_string = ''

    for elem in sorted(data_dict):
        check_string += f'{elem}={data_dict[elem]}\n'
    check_string = check_string.strip()
    
    logger.info(check_string)

    bot_secret_token = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()

    calculated_hash = hmac.new(
        bot_secret_token,
        check_string.encode(),
        sha256
    ).hexdigest()

    logger.info(calculated_hash)
    

    if calculated_hash != hash:
        raise ValueError('не верный hash')
    
    if calculated_hash == hash:
        return json.loads(data_dict['user'])