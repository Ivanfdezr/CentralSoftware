from functools import wraps
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import copy


def calculate_DragTorqueSideforce(self):

	MD = self.workWellboreMD
	Inc,Azi = mdl.get_inclination_and_azimuth_from_locations()