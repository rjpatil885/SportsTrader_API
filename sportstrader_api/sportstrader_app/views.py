from django.shortcuts import render, HttpResponse
import requests
from django.http import JsonResponse
from json import JSONDecodeError
import json

def home(request):

  try:
    url = 'https://api.sportradar.us/soccer/trial/v4/en/seasons/sr:season:77453/schedules.json'
    params = {'api_key': '77ynyjersbzwvrjnyyye37wf'}
    response = requests.get(url, params=params)
    data = response.json()
 
    event_info = []
    for schedule in data['schedules']:
      event = schedule['sport_event']
      competitors = event['competitors']
      status = schedule['sport_event_status']
      id = event['id']
    
      if 'home_score' in status:
        home_score = status['home_score']
      else:
        pass
      if 'away_score' in status:
        away_score = status['away_score']
      else:
        pass
      
      if 'period_scores' in status:
        period_scores = status['period_scores']
        halftime_score_home = period_scores[0]['home_score']
        halftime_score_away = period_scores[0]['away_score']
      else:
        pass
      
      home = competitors[0]['name']
      away = competitors[1]['name']


      event_info.append({
      'id' : id,
      'home_team': home,
      'away_team': away,
      'home_score': home_score,
      'away_score': away_score,
      'halftime_score_home': halftime_score_home,
      'halftime_score_away': halftime_score_away,
      'match_date': event['start_time'],
      'stadium': event['venue']['name']
      })
    
    url1 = f'https://api.sportradar.us/soccer/trial/v4/en/competitions/sr:competition:202/seasons.json'
    params1 = {'api_key': '77ynyjersbzwvrjnyyye37wf'}
    response1 = requests.get(url1, params=params1)
    cmp_id1 = response1.json()
    cmp_id = cmp_id1['seasons']
    return render(request,'home.html',  {'data': event_info,'cmp_id':cmp_id})
  except :
    return HttpResponse(f"Error:Unable to fetch JSON data correctly (Please Reload the page again) ")


def match_info(request, event_id):
  try:
      match_info_url = f'https://api.sportradar.us/soccer/trial/v4/en/sport_events/{event_id}/timeline.json'
      params = {'api_key': '77ynyjersbzwvrjnyyye37wf'}
      response = requests.get(match_info_url, params=params)
      data = response.json()
      
      event_info = {}

      if 'sport_event' in data:
        event = data['sport_event']
        info = data['sport_event_status']
        timeline_info = data['timeline']
        event_info = {
        'home_score' : info['home_score'],
        'away_score' : info['away_score'],
        'home_team': event['competitors'][0]['name'],
        'away_team': event['competitors'][1]['name'],
        'match_date': event['start_time'],
        'stadium': event['venue']['name'],
        'home_statistics' :data["statistics"]["totals"]['competitors'][0]['statistics'],
        'away_statistics' :data["statistics"]["totals"]['competitors'][1]['statistics'],
        'home_players' :data["statistics"]["totals"]['competitors'][0]['players'],
        'away_players' :data["statistics"]["totals"]['competitors'][1]['players'],
        'timeline':timeline_info,
          }

      return render(request, 'detail-matchinfo.html', {'data': event_info,'timeline':timeline_info})
  except :
    return HttpResponse(f"Error: unable to correctly retrieve JSON data from the api (Please reload the page again)")




def season_filter(request):

  try:
    filter_dict = request.GET.get('filter_dict')
    load_data = json.loads(filter_dict)
    season_filter = load_data.get("season_filter", None)
    quantity_filter = load_data.get("quantity_filter", None)
    print(season_filter)
    season_url  = f'https://api.sportradar.us/soccer/trial/v4/en/seasons/{season_filter}/schedules.json'
    params = {'api_key': '77ynyjersbzwvrjnyyye37wf'}

    response = requests.get(season_url, params=params)
    data = response.json()

    event_info = []
    for schedule in data['schedules']:
      event = schedule['sport_event']
      competitors = event['competitors']

      status = schedule['sport_event_status']
      id = event['id']
    
      if 'home_score' in status:
        home_score = status['home_score']
      else:
        pass
      if 'away_score' in status:
        away_score = status['away_score']
      else:
        pass
      
      if 'period_scores' in status:
        period_scores = status['period_scores']
        halftime_score_home = period_scores[0]['home_score']
        halftime_score_away = period_scores[0]['away_score']
      else:
        pass
      home = competitors[0]['name']
      away = competitors[1]['name']

      event_info.append({
      'id' : id,
      'home_team': home,
      'away_team': away,
      'home_score': home_score,
      'away_score': away_score,
      'halftime_score_home': halftime_score_home,
      'halftime_score_away': halftime_score_away,
      'match_date': event['start_time'],
      'stadium': event['venue']['name']
      })

    if quantity_filter == "all":
      event_info = event_info
    else:
      event_info = event_info[:int(quantity_filter)]
 
    return JsonResponse({'data':event_info}, safe=False)
  except:
    return HttpResponse(f"Error: unable to correctly retrieve JSON data from the api (Please reload the page again)")

def quantityFilter(request):

  try:

    filter_dict = request.GET.get('filter_dict')
    load_data = json.loads(filter_dict)
    season_filter = load_data.get("season_filter", None)
    quantity_filter = load_data.get("quantity_filter", None)

    qty_url = f'https://api.sportradar.us/soccer/trial/v4/en/seasons/{season_filter}/schedules.json'
    params = {'api_key': '77ynyjersbzwvrjnyyye37wf'}
    response = requests.get(qty_url, params=params)
    data = response.json()

    event_info = []
    for schedule in data['schedules']:
      event = schedule['sport_event']
      competitors = event['competitors']
      status = schedule['sport_event_status']
      id = event['id']
    
      if 'home_score' in status:
        home_score = status['home_score']
      else:
        pass
      if 'away_score' in status:
        away_score = status['away_score']
      else:
        pass
      
      if 'period_scores' in status:
        period_scores = status['period_scores']
        halftime_score_home = period_scores[0]['home_score']
        halftime_score_away = period_scores[0]['away_score']
      else:
        pass
      
      home = competitors[0]['name']
      away = competitors[1]['name']

      event_info.append({
      'id' : id,
      'home_team': home,
      'away_team': away,
      'home_score': home_score,
      'away_score': away_score,
      'halftime_score_home': halftime_score_home,
      'halftime_score_away': halftime_score_away,
      'match_date': event['start_time'],
      'stadium': event['venue']['name']
      })

    if quantity_filter == "all":
      event_info = event_info
    else:
      event_info = event_info[:int(quantity_filter)]
 
    return JsonResponse({'data':event_info}, safe=False)
  except:
    return HttpResponse(f"Error: unable to correctly retrieve JSON data from the api (Please reload the page again)")
  



from datetime import datetime

def dateFilter(request):

  try:
    filter_dict = request.GET.get('filter_dict')
    load_data = json.loads(filter_dict)
    season_filter = load_data.get("season_filter", None)
    quantity_filter = load_data.get("quantity_filter", None)
    date_filter = load_data.get("date_filter", None)

    url_filter = f'https://api.sportradar.us/soccer/trial/v4/en/seasons/{season_filter}/schedules.json'
    params = {'api_key': '77ynyjersbzwvrjnyyye37wf'}
    response = requests.get(url_filter, params=params)
    data = response.json()

    event_info = []
    
    for schedule in data['schedules']:
      event = schedule['sport_event']
      competitors = event['competitors']

      status = schedule['sport_event_status']
      id = event['id']
      date = event['start_time']

      date_str = date_filter[-4:] + "/" + date_filter[3:5] + "/" + date_filter[:2]
      cus_data = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").date()
      date_string_formatted = str(cus_data).replace("-","/")
      date_str= date_string_formatted[:4] + "/" + date_string_formatted[8:] + "/" + date_string_formatted[5:7]

      if date_str == date_str:
      
        home_score = status.get('home_score', None)
        away_score = status.get('away_score', None)
        period_scores = status.get('period_scores', None)

        if period_scores:
          halftime_score_home = period_scores[0]['home_score']
          halftime_score_away = period_scores[0]['away_score']
        else:
          halftime_score_home = None
          halftime_score_away = None

        home = competitors[0]['name']
        away = competitors[1]['name']

        event_info.append({
        'id': id,
        'home_team': home,
        'away_team': away,
        'home_score': home_score,
        'away_score': away_score,
        'halftime_score_home': halftime_score_home,
        'halftime_score_away': halftime_score_away,
        'match_date': date,
        'stadium': event['venue']['name']
        })
        
    if quantity_filter == "all":
      event_info = event_info
    else:
      event_info = event_info[:int(quantity_filter)]

      return JsonResponse({'data':event_info}, safe=False)
  except:
    return HttpResponse(f"Error: unable to correctly retrieve JSON data from the api (Please reload the page again)")

  

