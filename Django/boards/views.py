#from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import Http404
from .forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})



def board_topics(request, pk):
    try:
        board = Board.objects.get(pk = pk) #We can also use the get_object_or_404(Board, pk=pk) method and delete the try catch
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
                )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board':board, 'form':form})
