from django.shortcuts import render,redirect
from .models import Competitor
from django.http import JsonResponse
from .forms import AddLapScoreForm
from .decorators import superuser_required
from django.db.models import Case, When, Value, FloatField
from django.db.models.functions import Coalesce

# Create your views here.
def leaderboard_view(request, *args, **kwargs):
    #all_competitors = Competitor.objects.all()
    #context = {'competitors': all_competitors}
    context = {}
    return render(request, "leaderboard_app/leaderboard.html",context)

def leaderboard_update_api(request, *args, **kwargs):
    all_competitors = Competitor.objects.order_by(
        Case(
            When(current_best__lte=0, then=Value(9999)),
            default='current_best',
            output_field=FloatField(),
        )
    )
    
    #all_competitors = Competitor.objects.all()
    for competitor in all_competitors:
        competitor.update_current_best()
    data = [{'name': competitor.user.username, 'laps': ' '.join([str(lap) if lap > 0 else "X" for lap in competitor.laps]), 'score': str(competitor.current_best)} for competitor in all_competitors]
    return JsonResponse(data, safe=False)


@superuser_required
def add_lap_score(request, *args, **kwargs):
  if request.method == "POST":
      form = AddLapScoreForm(request.POST)
      if form.is_valid():
          selected_user = form.cleaned_data["user"]
          lap_score = form.cleaned_data["lap_score"]

          competitor, created = Competitor.objects.get_or_create(user=selected_user)
          if competitor.laps is not None:
              competitor.laps.append(lap_score)
          else:
              competitor.laps = [lap_score]
          competitor.save()

          return redirect("leaderboard_app:add_lap_score")  # Replace "some_view" with the desired view to redirect to
  else:
      form = AddLapScoreForm()
  return render(request, "leaderboard_app/add_lap_score.html", {"form": form})