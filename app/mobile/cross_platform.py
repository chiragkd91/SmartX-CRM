"""
Cross-platform Support for CRM System
"""

class CrossPlatformSupport:
    def __init__(self):
        self.platforms = ['ios', 'android', 'web', 'desktop']
        self.configs = {p: {} for p in self.platforms}
    def get_supported_platforms(self):
        return self.platforms
    def get_platform_config(self, platform):
        return self.configs.get(platform, {}) 