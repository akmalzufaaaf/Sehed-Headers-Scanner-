DEFAULT_URL_SCHEME = 'https'
DEFAULT_TIMEOUT = 10

# Browser-like request headers
REQUEST_HEADERS = {
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
               'application/signed-exchange;v=b3;q=0.9'),
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                   'Chrome/106.0.0.0 Safari/537.36'),
}

# Evaluation constants
EVAL_WARN = 0
EVAL_OK = 1
OK_COLOR = '\033[92m'
END_COLOR = '\033[0m'
WARN_COLOR = '\033[93m'
COLUMN_WIDTH_R = 12

# Security rules
UNSAFE_CSP_RULES = {
    "script-src": ["*", "'unsafe-eval'", "data:", "'unsafe-inline'", "http:"],
    "frame-ancestors": ["*"],
    "form-action": ["*"],
    "object-src": ["*"],
}

RESTRICTED_PERM_POLICY_FEATURES = ['camera', 'geolocation', 'microphone', 'payment']

SERVER_VERSION_HEADERS = [
    'x-powered-by',
    'server',
    'x-aspnet-version',
]

HEADER_STRUCTURED_LIST = [
    'permissions-policy',
]
