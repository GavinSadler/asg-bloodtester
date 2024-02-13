
CHANNELDATA_PHP_RESPONSE = ""
MYSQL2JSON_PHP_RESPONSE = ""

with open("./channeldata-php-dummyresponse.json", "r") as fp:
    CHANNELDATA_PHP_RESPONSE = fp.read()

with open("./mysql2json-php-dummy-response.json", "r") as fp:
    MYSQL2JSON_PHP_RESPONSE = fp.read()
