from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response, status
from .exceptions import NegativeTitlesError
from .exceptions import InvalidYearCupError
from .exceptions import ImpossibleTitlesError
from .models import Team
from .utils import data_processing


class CreateAndGetView(APIView):
    def post(self, request):
        bodyData = request.data

        status_bad_request = status.HTTP_400_BAD_REQUEST

        try:
            data_processing(bodyData)
        except NegativeTitlesError as error:
            return Response({"error": error.message}, status_bad_request)
        except InvalidYearCupError as error:
            return Response({"error": error.message}, status_bad_request)
        except ImpossibleTitlesError as error:
            return Response({"error": error.message}, status_bad_request)

        create_team = Team.objects.create(**bodyData)

        model_team = model_to_dict(create_team)

        return Response(model_team, status.HTTP_201_CREATED)

    def get(self, request):
        team_object = Team.objects.all()

        status_ok = status.HTTP_200_OK

        teams = [model_to_dict(team) for team in team_object]

        return Response(teams, status_ok)


class GetByIdAndPatchAndDeleteView(APIView):
    def get(self, request, team_id):
        status_not_found = status.HTTP_404_NOT_FOUND

        message_not_found = {"message": "Team not found"}

        status_ok = status.HTTP_200_OK

        try:
            get_by_id = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(message_not_found, status_not_found)

        model_team = model_to_dict(get_by_id)

        return Response(model_team, status_ok)

    def delete(self, request, team_id):
        status_not_found = status.HTTP_404_NOT_FOUND

        message_not_found = {"message": "Team not found"}
               
        status_no_content = status.HTTP_204_NO_CONTENT

        try:
            get_by_id = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(message_not_found, status_not_found)

        get_by_id.delete()

        return Response(status=status_no_content)

    def patch(self, request, team_id):
        status_ok = status.HTTP_200_OK

        message_not_found = {"message": "Team not found"}

        status_not_found = status.HTTP_404_NOT_FOUND

        try:
            get_by_id = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(message_not_found, status_not_found)

        for key, value in request.data.items():
            setattr(get_by_id, key, value)

        get_by_id.save()

        model_team = model_to_dict(get_by_id)

        return Response(model_team, status_ok)
