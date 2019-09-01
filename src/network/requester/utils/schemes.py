
class Schemes:
    allowable = ('http', 'https',)
    ports = {
        allowable[0]: 80,
        allowable[1]: 443
    }
    default = allowable[0]
