# -*- coding: utf8 -*-

import schedule

displays = []
def setup(config):
	logger = logging.getLogger(__name__)
	for finder, name, ispkg in pkgutils.walk_packages(['.']):
		if name == __name__: continue
		try:
			loader = finder.find_module(name)
			mod = loader.load_module(name)
		except:
			logger.warning("Skipped module '%s' due to an error.", name, exc_info=True)
	
	for disp in get_displays():
		instance = disp(config)
		schedule.every(instance.period()).seconds.do(instance.update)
		displays.append(instance)


class Display(object):
	def __init__(self, config):
		pass

	def period(self):
		return 1

	def update(self):
		pass

def get_displays():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [display for display in list(get_subclasses(Display))]
