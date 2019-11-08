import types
import importlib
	
def reload_modules():
	for name, val in globals().items():
		if isinstance(val, types.ModuleType):
			#yield name #val.__name__
			if name[:2]!='__' or name[-2:]!='__':
				print('Reloading: ',name,'in',__name__)
				try:
					importlib.reload(name)
				except TypeError:
					print('FAILED')
