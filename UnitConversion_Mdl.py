import re
import numpy as np
import codecs
import dbUtils
import MdlUtilities as mdl

def read_parameters():
	query = """select parameterName from parameters"""
	items = dbUtils.execute_query(query)

	lista = []

	for item in items:
		lista.append(item[0])
			
	print (lista)	

	return lista


def read_units(parameterX):
	query = """select u.representation from units u, parameters p
			where p.parameterName = '{parameter}' and p.quantityID = u.quantityID""".format(parameter=parameterX)	
	items = dbUtils.execute_query(query)

	units = []
	
	for item in items:
		units.append(item[0])
				
	return units


def calculate(originX,targetX,textX,placesX):
	value = float(textX)
	R = mdl.unitConvert_value( value, originX, targetX )
	return round(R,int(placesX))

	
def generate_binnacle(parameterX,originX,targetX,textX,placesX,result):
	query = """ insert into binnacle_conversion (Parameter,Unit_origin,Unit_target,Quantity_origin,Decimal_places, Result) 
			values ('{parameterX}','{originX}','{targetX}','{textX}','{placesX}','{result}')
			""".format(parameterX=parameterX,originX=originX, targetX=targetX, textX=textX, placesX=placesX, result=result)
	dbUtils.execute_query(query)
	
	
