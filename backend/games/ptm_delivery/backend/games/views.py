from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DailyPuzzle
from .services import check_guess, get_daily_puzzle


class TodayPuzzleView(APIView):
    """GET /api/games/23-guesses/today/

    Returns metadata + the first clue only. Never includes the answer.
    """

    def get(self, request):
        today = timezone.localdate()
        puzzle = get_daily_puzzle(today)

        if puzzle is None:
            return Response(
                {"detail": "No puzzles have been added yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "date": today.isoformat(),
                "puzzle_id": puzzle.id,
                "sport": puzzle.sport,
                "category": puzzle.category,
                "difficulty": puzzle.difficulty,
                "total_clues": len(puzzle.clues),
                "clue": puzzle.clues[0] if puzzle.clues else None,
            }
        )


class GuessView(APIView):
    """POST /api/games/23-guesses/guess/
    body: { puzzle_id, guess, clue_index }
    """

    def post(self, request):
        puzzle_id = request.data.get("puzzle_id")
        guess = request.data.get("guess", "")
        try:
            clue_index = int(request.data.get("clue_index", 0))
        except (TypeError, ValueError):
            return Response(
                {"detail": "clue_index must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not puzzle_id:
            return Response(
                {"detail": "puzzle_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            puzzle = DailyPuzzle.objects.get(id=puzzle_id)
        except DailyPuzzle.DoesNotExist:
            return Response(
                {"detail": "Puzzle not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Only allow guesses against whichever puzzle is actually "today's"
        # puzzle — stops someone from guessing against an arbitrary
        # puzzle_id to peek at clues that aren't live yet.
        today_puzzle = get_daily_puzzle(timezone.localdate())
        if today_puzzle is None or today_puzzle.id != puzzle.id:
            return Response(
                {"detail": "This puzzle isn't currently active."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = check_guess(puzzle, guess, clue_index)
        return Response(result)
