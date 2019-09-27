import hvac


class Credentials:

    def __init__(self):
        self.client = hvac.Client(
            url="http://vault:8200",
            token='s.bfV1qoOnS3RrgZv3yGEi9oJ9')

    def get_credentials(self, credential):

        credentials = None

        try:
            credentials = (
                self.client
                    .secrets
                    .kv
                    .read_secret_version(path=credential)
            ).get('data')

        except Exception as e:
            print(e)
            return credentials

        return credentials.get('data')


credentials = Credentials()
