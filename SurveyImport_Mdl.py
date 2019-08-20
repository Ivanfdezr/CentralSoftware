from MdlUtilities import Field, FieldList
import MdlUtilities as mdl
import dbUtils


def get_lengthUnits():

	query = 'select u.representation from units u, quantities q where u.quantityID=q.quantityID and q.quantityName="length"'
	items = dbUtils.execute_query(query)
	units = [ item[0] for item in items ]

	return units


def get_inclinationUnits():

	query = 'select u.representation from units u, quantities q where u.quantityID=q.quantityID and q.quantityName="inclination"'
	items = dbUtils.execute_query(query)
	units = [ item[0] for item in items ]

	return units

		 
def get_siSurveyData_fields():

	MD   = Field(2001, altBg=True, altFg=True)
	Inc  = Field(2002, altBg=True, altFg=True)
	Azi  = Field(2003, altBg=True, altFg=True)
	siSurveyData_fields = FieldList()
	siSurveyData_fields.append( MD  )
	siSurveyData_fields.append( Inc )
	siSurveyData_fields.append( Azi )
	
	return siSurveyData_fields


class HtmlRichText():

	def __init__( self ):
		
		self.hmtl_starting =  """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">
							<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head>
							<body style=\" font-family:\'Consolas\'; font-size:9pt; font-weight:400; font-style:normal;\">"""

		self.html_ending = "</body></html>"

		self.p_starting = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"

		self.p_ending = "</p>\n"

		self.__body__ = ''


	def get_html(self):

		return self.hmtl_starting + self.__body__ + self.html_ending


	def get_styledText( self, text, color, bold=False ): 
		
		if bold:
			return "<span style=\" font-weight:600; color:{color};\">{text}</span>".format(color=color, text=text)
		else:
			return "<span style=\" color:{color};\">{text}</span>".format(color=color, text=text)


	def add_line( self, text ):

		self.__body__ += self.p_starting + text + self.p_ending


	

