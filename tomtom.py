import requests
import zipfile
import pandas as pd
import io
import os

joblist_source = 'https://api.tomtom.com/traffic/trafficstats/job/search/1?key=RGiTCBAUhezwDp9Z7ftdw4Gxx16aZ3sB&name=SS_MEL_TomTom_Rel2016AWDT_v2%&pageIndex={}&type=routeanalysis&state=DONE'
summary_source = 'https://api.tomtom.com/traffic/trafficstats/status/1/{}?key=RGiTCBAUhezwDp9Z7ftdw4Gxx16aZ3sB'
pages = 111

all_jobs = []
job_summaries = []
seen = {}

# Find total job list
for x in range(0, pages):
    joblist = requests.get(joblist_source.format(x)).json()['content']

    for job in joblist:
        if job['id'] in seen:
            continue
        all_jobs.append(job)
        seen[job['id']] = True


# Find the summary for each job
print(all_jobs)
for job in all_jobs:
    excel_links = requests.get(summary_source.format(job['id'])).json()['urls']
    for link in excel_links:
        path, ext = os.path.splitext(link)
        extension = (ext.split('?')[0])

        if extension != '.json':
            continue

        res = requests.get(link).json()

        for route in res['routes']:
            for summary in route['summaries']:
                constructed_json = { 'id': job['id'] }
                constructed_json['name'] = res['jobName']
                constructed_json['timeSet'] = summary['timeSet']
                constructed_json['distance'] = summary['distance']
                constructed_json['averageSampleSize'] = summary['averageSampleSize']
                constructed_json['harmonicAverageSpeed'] = summary['harmonicAverageSpeed']
                constructed_json['averageTravelTime'] = summary['averageTravelTime']
                constructed_json['travelTimeStandardDeviation'] = summary['travelTimeStandardDeviation']
                constructed_json['85thPerSpeed'] = summary['speedPercentiles'][-3]
                constructed_json['90thPerSpeed'] = summary['speedPercentiles'][-2]
                constructed_json['95thPerSpeed'] = summary['speedPercentiles'][-1]
                constructed_json['routeName'] = route['routeName']
                i = 0
                while True:
                    segment = route['segmentResults'][i]
                    
                    try:
                        constructed_json['speedLimit'] = segment['speedLimit']
                        constructed_json['frc'] = segment['frc']
                        constructed_json['streetName'] = segment['streetName']
                        break
                    except:
                        i += 1
                        pass
                job_summaries.append(constructed_json)

print(job_summaries)
