import logging
import sys
import os
import json
import time

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
    
    testResults = {"results":[]}

    with client.ProxyKmipClient(
            hostname=hostname,
            port=port,
            cert=cert,
            key=key,
            ca=ca,
            config='client',
            config_file=opts.config_file
    ) as client:

        # operation_create
        try:
            uid = client.create(
                algorithm,
                length,
                operation_policy_name=opts.operation_policy_name
            )
            logger.info("Successfully created symmetric key with ID: "
                        "{0}".format(uid))

            testResults["results"].append({"operationName": "operation_create",
                                           "successful": True})
        
        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_create",
                                           "successful": False})
        # operation_activate
        try:
            result = client.activate(uid)
            logger.info("Successfully activated: {0}".format(uid))

            testResults["results"].append({"operationName": "operation_activate",
                                           "successful": True})
        
        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_activate",
                                           "successful": False})

        # operation_get
        try:
            secret = client.get(uid)
            logger.info("Successfully retrieved secret with ID: {0}".format(
                uid))
            logger.info("Secret data: {0}".format(secret))

            testResults["results"].append({"operationName": "operation_get",
                                           "successful": True})
        
        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_get",
                                           "successful": False})

        # operation_get_attributes
        try:
            _, attributes = client.get_attributes(uid, attribute_names=["State"])
            logger.info("Successfully retrieved {0} attributes:".format(
                len(attributes)))
            for attribute in attributes:
                logger.info("Attribute {0}: {1}".format(
                    attribute.attribute_name, attribute.attribute_value))

            testResults["results"].append({"operationName": "operation_get_attributes",
                                           "successful": True})
        
        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_get_attributes",
                                           "successful": False})

        # operation_revoke 
        try:
            client.revoke(
                enums.RevocationReasonCode.KEY_COMPROMISE,
                uid=uid,
                revocation_message="I want to revoke this secret.",
                compromise_occurrence_date=int(time.time())
            )
            logger.info(
                "Successfully revoked secret with ID: {0}".format(uid)
            )

            testResults["results"].append({"operationName": "operation_revoke",
                                           "successful": True})
        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_revoke",
                                           "successful": False})

        # operation_get_attribute_list
        try:
            attribute_names = client.get_attribute_list(uid)
            logger.info("Successfully retrieved {0} attribute names:".format(
                len(attribute_names)))
            for attribute_name in attribute_names:
                logger.info("Attribute name: {0}".format(attribute_name))

            testResults["results"].append({"operationName": "operation_get_attribute_list",
                                           "successful": True})

        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_get_attribute_list",
                                            "successful": False})

        # operation_destroy
        try:
            uid = client.create(
                algorithm,
                length,
                operation_policy_name=opts.operation_policy_name
            )
            client.destroy(uid)
            logger.info("Successfully destroyed secret with ID: {0}".format(
                uid))

            testResults["results"].append({"operationName": "operation_destroy",
                                           "successful": True})
        except Exception as e:
            logger.error(e)
            testResults["results"].append({"operationName": "operation_destroy",
                                            "successful": False})


        # Print JSON Results
        print(json.dumps(testResults))

        # Save JSON Result to file
        with open('results.json', 'w') as f:
            json.dump(testResults, f)
