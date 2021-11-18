import logging
import sys
import os

from kmip.core import enums
from kmip.demos import utils
from kmip.pie import client


if __name__ == '__main__':
    logger = utils.build_console_logger(logging.INFO)

    # Build and parse arguments
    parser = utils.build_cli_parser(enums.Operation.CREATE)
    opts, args = parser.parse_args(sys.argv[1:])

    config = opts.config

    algorithm = 'AES'
    length = 128

    algorithm = getattr(enums.CryptographicAlgorithm, algorithm, None)

    hostname = os.environ['KMIP_ADDR']
    port = os.environ['KMIP_PORT']
    cert = os.environ['KMIP_CERT']
    key = os.environ['KMIP_KEY']
    ca = os.environ['KMIP_CA']
    

    with client.ProxyKmipClient(
            hostname=hostname,
            port=port,
            cert=cert,
            key=key,
            ca=ca,
            config='client',
            #config_file=opts.config_file
    ) as client:
        try:
            # Create key
            uid = client.create(
                algorithm,
                length,
                operation_policy_name=opts.operation_policy_name
            )
            logger.info("Successfully created symmetric key with ID: "
                        "{0}".format(uid))

            # Get key
            secret = client.get(uid)
            logger.info("Successfully retrieved secret with ID: {0}".format(
                uid))
            logger.info("Secret data: {0}".format(secret))

            # Get attributes
            attribute_names = client.get_attribute_list(uid)
            logger.info("Successfully retrieved {0} attribute names:".format(
                len(attribute_names)))
            for attribute_name in attribute_names:
                logger.info("Attribute name: {0}".format(attribute_name))

            # Destroy Key
            client.destroy(uid)
            logger.info("Successfully destroyed secret with ID: {0}".format(
                uid))

        except Exception as e:
            logger.error(e)
