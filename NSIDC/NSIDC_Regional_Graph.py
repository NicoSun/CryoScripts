import pandas as pd
import matplotlib.pyplot as plt
#style.use('ggplot')


class Graph_Creater:

	def __init__  (self):
		self.year = 2021
		self.month = 1
		self.day = 1
			
		
			
	def area_graph(self,df,df_NRT,sheet_name,xxx):
		fig = plt.figure(figsize=(10, 6.5))
		fig.suptitle(str(sheet_name)+' - Sea Ice Area', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan']
		x = [0,30,59,90,120,151,181,212,243,273,304,334,366] # 1st Jan is day zero
		plt.xticks(x,labels)

		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		ax.text(0.02, 0.04, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.02, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/regional',transform=ax.transAxes,color='grey', fontsize=10)
		
		maximum = max(df['1980s']*1.1)
		ax.grid(True)
		plt.plot( df['1980s'], color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
		plt.plot( df['1990s'], color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
		plt.plot( df['2000s'], color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( df['2010s'], color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
		plt.plot( df['Min'], color=(0.6,0,0),label='Minimum',lw=1,ls='--')
		plt.plot( df_NRT, color=(0,0,0),label=f'{self.year}',lw=2)
		
		plt.axis([0,366,0,maximum])
		plt.legend(loc=1, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('temp/Area_{}.png'.format(xxx))
		plt.close()
		#plt.show()
		return
		 
	def extent_graph(self,df,df_NRT,sheet_name,xxx):
		fig = plt.figure(figsize=(10, 6.5))
		fig.suptitle(str(sheet_name)+' - Sea Ice Extent', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan']
		x = [0,30,59,90,120,151,181,212,243,273,304,334,366] # 1st Jan is day zero
		plt.xticks(x,labels)

		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		ax.text(0.72, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.72, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/regional',transform=ax.transAxes,color='grey', fontsize=10)
		
		maximum = max(df['1980s']*1.1)
		ax.grid(True)
		plt.plot( df['1980s'], color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
		plt.plot( df['1990s'], color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
		plt.plot( df['2000s'], color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( df['2010s'], color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
		plt.plot( df['Min'], color=(0.6,0,0),label='Minimum',lw=1,ls='--')
		plt.plot( df_NRT, color=(0,0,0),label=f'{self.year}',lw=2)
		
		plt.axis([0,366,0,maximum])
		plt.legend(loc=2, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('temp/Extent_{}.png'.format(xxx))
		#plt.show()
		plt.close()
		return
	
	def loadRegionaldata(self):
		
		df_NRT = pd.read_csv('Regional_2020.csv')
		df_NRT.drop(['Date'], 1, inplace=True)
		column_names = df_NRT.columns
		
		excelfile = 'Regional_Climate.xlsx'
		for xxx in range(0,13):	#13 regional
			df = pd.read_excel(excelfile,sheet_name=xxx)
			
			xls = pd.ExcelFile(excelfile)
			sheet_name = xls.sheet_names[xxx]
			self.area_graph(df,df_NRT[column_names[xxx]],sheet_name,xxx+1)
			
			
	def loadRegionaldata_extent(self):
		df_NRT = pd.read_csv('Regional_2020.csv')
		df_NRT.drop(['Date'], 1, inplace=True)
		column_names = df_NRT.columns
		
		excelfile = 'Regional_Climate_extent.xlsx'
		for xxx in range(0,13):	#13 regional
			df = pd.read_excel(excelfile,sheet_name=xxx)
			
			xls = pd.ExcelFile(excelfile)
			sheet_name = xls.sheet_names[xxx]
			self.extent_graph(df,df_NRT[column_names[xxx]],sheet_name,xxx+1)
#


action = Graph_Creater()
if __name__ == "__main__":
	print('main')
# 	action.loadRegionaldata()
	action.loadRegionaldata_extent()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA