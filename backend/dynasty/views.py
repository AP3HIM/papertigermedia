from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import engine


class NewGameView(APIView):
    """POST /api/dynasty/new-game/
    body (optional): { city, team_name, philosophy }

    `philosophy` is one of: win_now, development, small_market, superteam.
    Defaults to win_now if omitted or unrecognized.
    """

    def post(self, request):
        city = request.data.get("city", "")
        team_name = request.data.get("team_name", "")
        philosophy = request.data.get("philosophy", "win_now")
        return Response(engine.new_game(city=city, team_name=team_name, philosophy=philosophy))


class AdvanceView(APIView):
    """POST /api/dynasty/advance/
    body: { state, choices }

    `choices` is a list of 0+ option objects the frontend displayed and
    the player picked this offseason (e.g. one draft option + one or more
    free-agent options + a trade offer). Each is echoed back exactly as
    shown — with its `prospect`, `depth_signees`, and/or `trade_give_slot`
    data — so whoever joins/leaves the roster matches what was on the card.
    """

    def post(self, request):
        state = request.data.get("state")
        choices = request.data.get("choices")

        if not state:
            return Response(
                {"detail": "state is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = engine.advance_dynasty(state, choices)
        except (KeyError, StopIteration, TypeError, ValueError) as exc:
            return Response(
                {"detail": f"Couldn't advance the dynasty: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result)


class ResolveSituationView(APIView):
    """POST /api/dynasty/resolve-situation/
    body: { state, situation_id, choice_id, context, made_playoffs, wins }

    `context` is the exact context dict the frontend was shown alongside
    the situation (e.g. {"player_name": "..."}) — echoed back so the
    resolution matches what was displayed.

    `made_playoffs` / `wins` are optional, taken from the season_result the
    frontend already has in hand. When present, the response includes a
    freshly-regenerated `next_decision` built from the POST-situation
    state (roster/cap after the situation's effects) instead of the
    decision options generated before the situation happened — this is
    what makes something like a forced release or a cap cut actually
    show up in the choices you're offered next, instead of the situation
    resolving against a roster the decision screen doesn't know about
    yet. If omitted, `next_decision` comes back null and the frontend
    should keep using whatever `decision` it already had.
    """

    def post(self, request):
        state = request.data.get("state")
        situation_id = request.data.get("situation_id")
        choice_id = request.data.get("choice_id")
        context = request.data.get("context") or {}
        made_playoffs = request.data.get("made_playoffs")
        wins = request.data.get("wins")

        if not state or not situation_id or not choice_id:
            return Response(
                {"detail": "state, situation_id, and choice_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = engine.resolve_situation(
                state, situation_id, choice_id, context=context,
                made_playoffs=made_playoffs, wins=wins,
            )
        except (KeyError, StopIteration, TypeError, ValueError) as exc:
            return Response(
                {"detail": f"Couldn't resolve that situation: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result)