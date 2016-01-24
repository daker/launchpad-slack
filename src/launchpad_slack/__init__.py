try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('launchpad-slack').version
except Exception, e:
    VERSION = 'unknown'
