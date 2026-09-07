from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import engine


class NewGameView(APIView):
    """POST /api/dynasty/new-game/
    body (optional): { city, team_name }
    """

    def post(self, request):
        city = request.data.get("city", "")
        team_name = request.data.get("team_name", "")
        return Response(engine.new_game(city=city, team_name=team_name))


class AdvanceView(APIView):
    """POST /api/dynasty/advance/
    body: { state, choice_id, chosen_option }

    `chosen_option` is the exact option object the frontend displayed —
    echoed back (with its `prospect` and/or `depth_signees` data) so
    whoever joins the roster matches what was shown on the card.
    """

    def post(self, request):
        state = request.data.get("state")
        choice_id = request.data.get("choice_id")
        chosen_option = request.data.get("chosen_option") or {}
        prospect = chosen_option.get("prospect")
        depth_signees = chosen_option.get("depth_signees")

        if not state or not choice_id:
            return Response(
                {"detail": "state and choice_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = engine.advance_dynasty(
                state, choice_id, prospect=prospect, depth_signees=depth_signees
            )
        except (KeyError, StopIteration, TypeError, ValueError) as exc:
            return Response(
                {"detail": f"Couldn't advance the dynasty: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result)
