import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import matplotlib.gridspec as gridspec
from matplotlib.gridspec import GridSpecFromSubplotSpec

# note: all the csv file names are with same name and the file name must ends with integer # for Reading csv files in order
new_file=sorted(glob("chapter_two*"))
# for merging all csv files into single file 
merge_data=pd.concat(pd.read_csv(datafile).assign(sourcefilename=datafile) for datafile in new_file)
# for Resetting the index of the merged csv file
merge_data=merge_data.reset_index()
print(merge_data)
# for delting the extra unwanted data in the merged csv file
del merge_data["index"]
del merge_data["Units"]
del merge_data["sourcefilename"]

# assigning new column names 
new_column_names=[]
for k in range(len(merge_data.columns)):
    if(k==0): 
        new_column_names.append("Investigation")
    elif(k==1): 
        new_column_names.append("Result")
    elif(k==2):
        new_column_names.append("Normal Ranges")
    else: 
        new_column_names.append(merge_data.columns[k])
merge_data.columns=new_column_names 

results=[]
testname=[]
interval=[] 
Results=merge_data['Result'] 
Testname=merge_data['Investigation'] 
Interval=merge_data['Normal Ranges']
for k in range(len(Testname)):
    testname.append(Testname[k]) 
for j in range(len(Results)):
    results.append(Results[j]) 
for m in range(len(Interval)):
    interval.append(Interval[m]) 

print(interval)
indexes=[]
for l in range(len(interval)):
    if type(interval[l])==float: 
        indexes.append(l)
print(indexes)

# for deleting the main test names and its related values in the arrays 
for i in range(len(indexes)):
    results.pop(indexes[i]-i) 
    testname.pop(indexes[i]-i) 
    interval.pop(indexes[i]-i)
result=[]
for i in results:
    if(type(i)==str): 
        i=i.replace(',','.')
    result.append(float(i))
  
# for creating the data frame only for testname and plotting points 
data={'Test Name':testname,'Result':results} 
df=pd.DataFrame(data)

lower_limit=[]
upper_limit=[]
array=[]
array1=[]
for i in interval:
    j= i.replace('_', ' ').replace(', ', ' ').replace('-', ' ').replace('mg/dl', ' ').replace('mg/dL', ' ').replace('UP TO','0 ').replace('U/L', ' ').replace('gm/dl', ' ').replace('gms/dl', ' ').replace('mill/cumm','').replace('/uL','').replace('%', ' ').replace('Lakhs/cumm','').replace('fL','').replace('pg','').replace('gms', ' ').replace('CHILDRENS', ' ').replace('ADULTS', ' ').replace('<', '0 ').replace('>', '100 ').replace('g/dL', ' ').replace('mg/dL', ' ').replace('mEq/L', ' ').replace('ng/mL', ' ').replace('ug/dL', ' ').replace('ulU/mL', ' ').replace('mill/mm3', ' ').replace('thou/mm3', ' ').replace('mm/hr', ' ').split()
    if(len(j)>2):
        print("hi")
        for k in range(len(j)):
            array1.append(float(j[k])) 
        array1=sorted(array1) 
        low=str(array1[0]) 
        high=str(array1[-2]) 
        j=[low,high]
    else:    
        pass
    array.append(j)

array2=[]
for i in range(len(array)):
    for j in range(len(array[i])):
        array2.append(float(array[i][j]))
plotting_points=[]

for i in range(len(array2)):
    if i%2==0:
        lower_limit.append(array2[i])
    else:
        upper_limit.append(array2[i])  
for i in range(len(result)):
    if(result[i]<lower_limit[i]): 
        plotting_points.append(1)
    elif(result[i]>upper_limit[i]): 
        plotting_points.append(3)
    else: 
        plotting_points.append(2)   
print(plotting_points) 

data={'Test Name':testname,'Condition':plotting_points} 
df=pd.DataFrame(data)

health_file=pd.read_csv("source_health_file.csv") 
new_test_names=[]
problem_d=[] 
new_med=[] 
new_cul=[] 
state=[] 
reason=[]
for i in range(len(df.loc[:,'Test Name'])):
    for j in range(len(health_file['Test'])):
        if(df['Test Name'][i]==health_file['Test'][j]):
             if(df['Condition'][i]==health_file['State'][j]):
                new_test_names.append(health_file['Test'][j]) 
                new_med.append(health_file['Medicine'][j]) 
                new_cul.append(health_file['Culture'][j]) 
                state.append(health_file['State'][j])
                reason.append(health_file['Reason'][j])
new_data_sheet={'Test':new_test_names,'State':state,'Reason':reason,'Medicine':new_med,'Culture':new_cul}
newdf=pd.DataFrame(new_data_sheet)
print(df)
print(newdf)

fig = plt.figure()

gs0 = gridspec.GridSpec(1, 1, figure=fig)

gs00 = gridspec.GridSpecFromSubplotSpec(5, 4, subplot_spec=gs0[0])


ax1 = fig.add_subplot(gs00[:-1, :-1])
i=df['Test Name']
j=df['Condition']
tt=newdf['Reason'].values 
tt1=newdf['Medicine'].values 
tt2=newdf['Culture'].values 

plt.plot(i,j)
scatter = plt.scatter(i, j, marker="*")
plt.xticks(rotation=90) 
ylab=["",'below\nnormal','normal','above\nnormal',"",""] 
plt.gca().set_yticks(range(len(ylab))) 
plt.gca().set_yticklabels(ylab)
plt.title("Total Health Analysis")
plt.xlabel("   Test Names")
plt.ylabel("Condition")
ax2 = fig.add_subplot(gs00[:,-1])
plt.axis('off') 
texth=ax2.text(0.3, 0.75,"Reason :",horizontalalignment='right',verticalalignment='top',wrap='True',fontsize=11,transform=ax2.transAxes)
text1h=ax2.text(0.3, 0.50,"Medicine :",horizontalalignment='right',verticalalignment='top',wrap='True',fontsize=11,transform=ax2.transAxes)
text2h=ax2.text(0.3, 0.25,"Food Culture :",horizontalalignment='right',verticalalignment='top',wrap='True',fontsize=11,transform=ax2.transAxes)
text_display = ax1.annotate("", xy=(0,0), xytext=(5,5),textcoords="offset points",bbox=dict(boxstyle='round',fc='linen',ec='k',lw=1),wrap='True')
text_display.set_visible(True)
text_display1 = ax2.annotate("", xy=(0.02,0.55), xytext=(5,5),textcoords="offset points",bbox=dict(boxstyle='round',fc='linen',ec='k',lw=1),wrap='True')
text_display1.set_visible(True)
text_display2 = ax2.annotate("", xy=(0.02,0.30), xytext=(5,5),textcoords="offset points",bbox=dict(boxstyle='round',fc='linen',ec='k',lw=1),wrap='True')
text_display2.set_visible(True)
text_display3 = ax2.annotate("", xy=(0.02,0.05), xytext=(5,5),textcoords="offset points",bbox=dict(boxstyle='round',fc='linen',ec='k',lw=1),wrap='True')
text_display3.set_visible(True)

def motion_hover(event):
    annotation_visbility = text_display.get_visible() 
    if event.inaxes == ax1:
        is_contained, annotation_index = scatter.contains(event) 
        if is_contained:
            data_point_location = scatter.get_offsets()[annotation_index['ind'][0]] 
            text_display.xy = data_point_location
            text_label1 = '{}'.format([tt[n] for n in annotation_index['ind']])
            text_display1.set_text(text_label1)
            text_display1.set_visible(True)
            text_label2 = '{}'.format([tt1[n] for n in annotation_index['ind']])
            if(text_label2 == "['No Need to use any Medicine']"):
                text_display2.set_text(text_label2)
            else:
                text_label2 += '\n[Please Contact Doctor Before Use]'
                text_display2.set_text(text_label2)
            text_display2.set_visible(True)
            text_label3 = '{}'.format([tt2[n] for n in annotation_index['ind']])
            text_display3.set_text(text_label3)
            text_display3.set_visible(True) 
            fig.canvas.draw_idle()
        else:
            if annotation_visbility:
                text_display1.set_visible(False)
                text_display2.set_visible(False)
                text_display3.set_visible(False)
                fig.canvas.draw_idle() 
fig.canvas.mpl_connect('motion_notify_event', motion_hover)

plt.show()