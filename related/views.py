from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    if request.method == "POST":
        name = request.POST['movie']
        limit = request.POST['limit']
        movies = get_movies_from_tastedive(name, limit=limit)
        return render(request, 'index.html',{
            "name":name.upper(),
            "movie_list": movies
        })
    return render(request, 'index.html')

def get_movies_from_tastedive(q,t = 'movies',limit = 5):
    para = {}
    para['q'] = q
    para['type'] = t
    para['limit'] = limit
    baseurl = 'https://tastedive.com/api/similar'
    res = requests.get(baseurl, params = para)
    movies = {}
    p = {}
    baseurl2 = 'http://www.omdbapi.com/'
    p['apikey'] = '8131eeb6'
    data = res.json()
    for d in data['Similar']['Results']:
        #movies.append(d['Name'])
        p['t'] = d['Name']        
        res2 = requests.get(baseurl2, params = p)
        data2 = res2.json()
        r = [item['Value'] for item in data2['Ratings'] if 'Rotten Tomatoes' in item['Source']]
        #r =(data2['Ratings'][1]['Value'])
    
        
        if len(r) != 0:
            r = float(''.join([i for i in r[0] if i != '%']))       
            movies[d['Name']] = r
        else:
            movies[d['Name']] = 0.0
    print(movies)   
    movies = sorted(movies, key = lambda x: movies[x], reverse=True)
    

    return [key for key in movies]