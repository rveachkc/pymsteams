from .base import Base


class AdaptiveCard(Base):
    def __init__(self, hookurl, http_proxy=None, https_proxy=None, http_timeout=60, verify=None):
        super().__init__(hookurl, http_proxy, https_proxy, http_timeout, verify)

        pass
