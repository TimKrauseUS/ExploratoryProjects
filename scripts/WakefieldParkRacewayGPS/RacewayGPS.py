def addPolyline(lap, apArr, cursor, sr, time, avg_speed):
    polyline = arcpy.Polyline(apArr,sr)
    cursor.insertRow((polyline, int(lap), round(time,2), round(avg_speed,2)))
    apArr.removeAll()
    

def insertLap(fcName, lap, lap_df, sr, time):
    with arcpy.da.InsertCursor(fcName, ("SHAPE@", "Lap", "LapTime", "AvgSpeed")) as cursor:
        #find average speed
        avg_speed = sum(lap_df['Speed (KM/H)']) / lap_df.count()[0]
        
        #create an empty ap.array
        apArr = arcpy.Array()
        
        #loop through lap_df to create points and add to array
        for lon, lat in zip(lap_df['Longitude'], lap_df['Latitude']):
            vertex = arcpy.Point(lon,lat)
            apArr.add(vertex)
        
        #add points to shp
        addPolyline(lap, apArr, cursor, sr, time, avg_speed)
    del cursor
            
            
import pandas as pd
import numpy as np
import arcpy
from arcpy import env
env.overwriteOutput = True


#set workspace
workspace = arcpy.GetParameterAsText(0) #r"D:\PENN_GEOG485\Lesson4\Project4"
env.workspace = workspace

#import data
df = pd.read_csv(arcpy.GetParameterAsText(1)) #"D:\PENN_GEOG485\Lesson4\Project4\WakefieldParkRaceway_20160421.csv")
#df.fillna(np.NaN)

#create feature class and add lap field
fcName = arcpy.GetParameterAsText(2) #"RacewayLaps.shp"
if '.shp' not in fcName: fcName += '.shp'
sr = arcpy.SpatialReference(4326)
arcpy.management.CreateFeatureclass(workspace, fcName, 'POLYLINE', spatial_reference=sr)
arcpy.management.AddField(fcName, 'Lap', 'SHORT')
arcpy.management.AddField(fcName, 'LapTime', 'FLOAT')
arcpy.management.AddField(fcName, 'AvgSpeed', 'FLOAT')

#number of laps completed
numLaps = max(df["Lap"])

# for num of laps, create df for each and use function to create the polyline
# also get lap time in seconds and add

# NOTE: lap 0 is warm-up lap (omit)
# NOTE: lap n(last) driver goes to pit (omit)
row = 0
for lap in np.arange(0,numLaps):
    lap_df = df[df["Lap"] == lap]
    
    #get lap times
    row += (lap_df.count()[0])
    time = float(df.iloc[row][0].split(':')[2])*60 + float(df.iloc[row][0].split(':')[3])
    row +=1
    
    
    if lap != 0:
        print("-- Adding Lap {} --".format(int(lap)))
        print("Lap {} has {} vertices.".format(int(lap),lap_df.count()[0]))
        print("Lap time {} seconds.".format(round(time,2)))
        insertLap(fcName, lap, lap_df, sr, time)

print("-- Complete!    --")
    


