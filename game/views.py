import json
from matplotlib.dates import DateFormatter
from django.db.models import Count, Sum, F, Func, IntegerField,ExpressionWrapper, fields
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import MemoryGameResult,MathQuizScore,MemoryMeastroScore,HitTheCatScore
from django.http import JsonResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns


# Create your views here.
def allgames(request):
    return render(request, 'allgames.html', {})


@login_required(login_url='/login')
def hangman(request):
    return render(request, 'hangman.html', {})


@login_required(login_url='/login')
def pixelart(request):
    return render(request, 'pixelart.html', {})


@csrf_exempt
@login_required(login_url='/login')
def memorycardgame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            moves = data.get('moves')
            time = data.get('time')
            user = request.user
            MemoryGameResult.objects.create(user=user, moves=moves, time=time)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'memorycard.html', {})


@login_required(login_url='/login')
def memory_game_analysis(request):
    import pandas as pd
    # Fetch data from the database for the logged-in user
    user_data = MemoryGameResult.objects.filter(user=request.user)
    moves=[]
    date=[]
    user=[]
    time=[]
    year=[]
    for i in range(0,len(user_data)):
        user.append(user_data[i].user)
        moves.append(user_data[i].moves)
        date.append(user_data[i].timestamp.date())
        time.append(user_data[i].time)
        # year.append(user_data[i].timestamp.year())
        print(time)

    data = {
        'User': user,
        'Moves': moves,
        'Date': date,
        'Time': time,
    }


    df = pd.DataFrame(data)

    print(df)
    min = df['Time'].str.split(':').str[0].astype(int)
    print(min)
    sec = df['Time'].str.split(':').str[1].astype(int)

    df['TotalMinutes'] = min+sec/60
    print(df)

    print(df.info())
    sns.lineplot(x='TotalMinutes', y='Moves', hue='User', data=df, marker='*')

    # Customize the plot
    plt.title('Memory Game Analysis')
    plt.xlabel('Time duration')
    plt.ylabel('Number of Moves')
    plt.legend(title='User', loc='upper left')

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the BytesIO object to base64 for embedding in HTML
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Pass the base64-encoded image to the template


    sns.lineplot(x='Date', y='Moves', hue='User', data=df, marker='*')
    plt.title('Memory Game Analysis')
    plt.xlabel('Date')
    plt.ylabel('Number of Moves')
    plt.legend(title='User', loc='upper left')
    # Format x-axisdates nicely

    # Save the graph to a BytesIO object
    image_stream1 = BytesIO()
    plt.savefig(image_stream1, format='png')
    plt.close()

    # Encode the BytesIO object to base64 for embedding in HTML
    image_base641 = base64.b64encode(image_stream1.getvalue()).decode('utf-8')

    # Pass the base64-encoded image to the template
    context =  {'image_base64': image_base64,'image_base641': image_base641}
    return render(request, 'memory_game_analysis.html', context)


@login_required(login_url='/login')
def flagmatchergame(request):
    return render(request, 'flagmatcher.html', {})


@login_required(login_url="/login")
def numberpuzzle(request):
    return render(request,'numberpuzzle.html',{})


@login_required(login_url="/login")
def simongame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            level = data.get('level')
            user = request.user
            print(level)
            MemoryMeastroScore.objects.create(user=request.user, level=level)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request,'simon.html',{})


@login_required(login_url="/login")
def memory_score_graph(request):
    # Retrieve logged-in user
    user = request.user

    # Query the database for the user's memory scores
    scores = MemoryMeastroScore.objects.filter(user=user)

    # Extract data for plotting
    levels = [score.level for score in scores]
    dates = [score.date.strftime('%b %d, %Y') for score in scores]

    # Plot the graph
    plt.figure(figsize=(14, 8))
    plt.plot(dates, levels, marker='o')
    plt.title(f'Memory Maestro Scores for {user.username}')
    plt.xlabel('Date',fontsize=14)
    plt.ylabel('Level',fontsize=14)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tick_params(axis='both', which='major', labelsize=12)

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the BytesIO object to base64 encoding
    image_data = base64.b64encode(buffer.read()).decode('utf-8')

    # Close the plot to release resources
    plt.close()

    # Pass the base64 encoded image data to the template
    context = {'image_data': image_data}
    return render(request, 'simon_game_analysis.html', context)


@login_required(login_url="/login")
def hitthecatgame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            score = data.get('score')
            gamespeed=data.get('gamespeed')
            time=data.get('timeleft')
            print(score,gamespeed,time)
            HitTheCatScore.objects.create(user=request.user, score=score,gamespeed=gamespeed,time=time)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request,'hitthecat.html',{})


@csrf_exempt
@login_required(login_url="/login")
def mathquizgame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            score = data.get('score')
            user = request.user
            MathQuizScore.objects.create(user=request.user, score=score)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request,'mathquiz.html',{})


