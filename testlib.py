import MdlUtilities as mdl

def get_centralizersLocations(self, ax):
	K = list(self.wellboreInnerStageData.keys())
	K.sort() #CentralizerProps
	for k in K:
		if self.wellboreInnerStageData[k]['Centralization']['Mode'] == 'by Spacing':
			spacing = self.wellboreInnerStageData[k]['Centralization']['A']['CentralizerProps'].Spacing[0]
			md0=self.s2DataSurvey_fields.MD[0] if k==0 else self.wellboreInnerStageData[k-1]['MD']
			md1=self.wellboreInnerStageData[k]['MD']
			
			print(k,md0)

			MDc = []
			EW = []
			NS = []
			VD = []
			while md0<md1:
				MDc.append(md0)
				md0 += spacing

			print(MDc)

			for mdc in MDc:
				for i, mdi in enumerate(self.s2DataSurvey_fields.MD):
					if mdi>mdc:
						i-=1 
						break
				mdc = mdl.referenceUnitConvert_value( mdc, self.s2DataSurvey_fields.MD.unit )
				sT_value = self.sT(i,mdc)
				ewc = mdl.inverseReferenceUnitConvert_value( sT_value[0], self.s2DataSurvey_fields.EW.unit  )
				nsc = mdl.inverseReferenceUnitConvert_value( sT_value[1], self.s2DataSurvey_fields.NS.unit  )
				vdc = mdl.inverseReferenceUnitConvert_value( sT_value[2], self.s2DataSurvey_fields.TVD.unit )

				EW.append(self.s2DataSurvey_fields.EW[i]+ewc)
				NS.append(self.s2DataSurvey_fields.NS[i]+nsc)
				VD.append(self.s2DataSurvey_fields.TVD[i]+vdc)

			ax.plot( EW, NS, VD, marker='o', color='C'+str(k), ls='' )