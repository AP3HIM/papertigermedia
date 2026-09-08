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


class ResolveSituationView(APIView):
    """POST /api/dynasty/resolve-situation/
    body: { state, situation_id, choice_id, context }

    `context` is the exact context dict the frontend was shown alongside
    the situation (e.g. {"player_name": "..."}) — echoed back so the
    resolution matches what was displayed.
    """

    def post(self, request):
        state = request.data.get("state")
        situation_id = request.data.get("situation_id")
        choice_id = request.data.get("choice_id")
        context = request.data.get("context") or {}

        if not state or not situation_id or not choice_id:
            return Response(
                {"detail": "state, situation_id, and choice_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = engine.resolve_situation(state, situation_id, choice_id, context=context)
        except (KeyError, StopIteration, TypeError, ValueError) as exc:
            return Response(
                {"detail": f"Couldn't resolve that situation: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result)
