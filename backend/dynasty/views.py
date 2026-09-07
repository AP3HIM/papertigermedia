from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import engine


class NewGameView(APIView):
    """GET /api/dynasty/new-game/ — bootstraps a fresh dynasty. No
    persistence: the frontend holds onto everything this returns."""

    def get(self, request):
        return Response(engine.new_game())


class AdvanceView(APIView):
    """POST /api/dynasty/advance/
    body: { state, choice_id, chosen_option }

    `chosen_option` is the exact option object the frontend displayed
    (including its `prospect` scouting profile, for draft/trade choices) —
    echoed back so the player who joins the roster is the same one shown
    on the card, not a freshly regenerated one.
    """

    def post(self, request):
        state = request.data.get("state")
        choice_id = request.data.get("choice_id")
        chosen_option = request.data.get("chosen_option") or {}
        prospect = chosen_option.get("prospect")

        if not state or not choice_id:
            return Response(
                {"detail": "state and choice_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = engine.advance_dynasty(state, choice_id, prospect=prospect)
        except (KeyError, StopIteration, TypeError, ValueError) as exc:
            return Response(
                {"detail": f"Couldn't advance the dynasty: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result)
