import requests

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.entity.webhooks import WebhookType
from ytrss.core.helpers.logging import logger


class WebhookManager:
    """
    Webhook Manager

    That object is responsible for managing webhooks. It can store and invoke webhook when its necessary. All
    webhooks should be defined in WebhookType, it has different name and set of arguments.
    """

    def __init__(self, configuration: YtrssConfiguration) -> None:
        self._configuration = configuration

    def invoke_hook(self, webhook: WebhookType) -> None:
        """ Invoke a webhook """

        logger.debug("[Webhook] Invoke Webhook: %s", webhook.name)
        for webhook_url in self._configuration.get_webhook(webhook.name):
            webhook_url_formated = webhook_url.format(**webhook.data)
            try:
                response = requests.get(webhook_url_formated, timeout=10)

                if response.status_code == 200:
                    logger.debug("[Webhook] Invoke url webhook: %s, %s", webhook.name, webhook_url_formated)
                else:
                    logger.error(
                        "[Webhook] Address url (%s) has %s output code",
                        webhook_url_formated,
                        response.status_code
                    )
            except requests.exceptions.RequestException as e:
                logger.error("[Webhook] Problem with request (%s): %s", webhook_url_formated, str(e))
