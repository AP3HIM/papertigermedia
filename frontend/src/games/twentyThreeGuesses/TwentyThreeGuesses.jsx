import { useEffect, useMemo, useState } from "react";
import { getTodayPuzzle, submitGuess } from "../../lib/api";
import { readProgress, recordResult, writeProgress, getStreak } from "./storage";
import "./TwentyThreeGuesses.css";

const STATUS = { LOADING: "loading", ERROR: "error", PLAYING: "playing", WON: "won", LOST: "lost" };

function buildShareText({ dateStr, totalClues, guessCount, won, score, streak }) {
  const filled = Math.min(guessCount, totalClues);
  const blocks = Array.from({ length: totalClues }, (_, i) =>
    i < filled - 1 ? "▪" : i === filled - 1 ? (won ? "■" : "▪") : "▫"
  ).join(" ");

  const result = won ? `Solved in ${guessCount}/${totalClues}` : `Didn't solve it (${totalClues}/${totalClues})`;

  return [`23 GUESSES — ${dateStr}`, result, blocks, `Score: ${score} · Streak: ${streak}`].join("\n");
}

export default function TwentyThreeGuesses() {
  const [status, setStatus] = useState(STATUS.LOADING);
  const [error, setError] = useState(null);
  const [puzzle, setPuzzle] = useState(null); // { date, puzzle_id, sport, category, difficulty, total_clues }
  const [revealedClues, setRevealedClues] = useState([]);
  const [guesses, setGuesses] = useState([]); // [{ text, correct }]
  const [inputValue, setInputValue] = useState("");
  const [answer, setAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data = await getTodayPuzzle();
        if (cancelled) return;

        setPuzzle(data);
        setStreak(getStreak());

        const saved = readProgress(data.date);
        if (saved && saved.puzzleId === data.puzzle_id) {
          setRevealedClues(saved.revealedClues);
          setGuesses(saved.guesses);
          setAnswer(saved.answer);
          setScore(saved.score);
          setStatus(saved.status);
        } else {
          setRevealedClues([data.clue]);
          setStatus(STATUS.PLAYING);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Couldn't load today's puzzle.");
          setStatus(STATUS.ERROR);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const clueIndex = revealedClues.length - 1;
  const isOver = status === STATUS.WON || status === STATUS.LOST;

  const shareText = useMemo(() => {
    if (!puzzle || !isOver) return "";
    return buildShareText({
      dateStr: puzzle.date,
      totalClues: puzzle.total_clues,
      guessCount: guesses.length,
      won: status === STATUS.WON,
      score,
      streak,
    });
  }, [puzzle, isOver, guesses.length, status, score, streak]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!inputValue.trim() || submitting || isOver) return;

    setSubmitting(true);
    try {
      const result = await submitGuess({
        puzzleId: puzzle.puzzle_id,
        guess: inputValue,
        clueIndex,
      });

      const nextGuesses = [...guesses, { text: inputValue, correct: result.correct }];
      let nextRevealedClues = revealedClues;
      let nextStatus = STATUS.PLAYING;
      let nextAnswer = answer;
      let nextScore = score;

      if (result.correct) {
        nextStatus = STATUS.WON;
        nextAnswer = result.answer;
        nextScore = result.score;
      } else if (result.out_of_clues) {
        nextStatus = STATUS.LOST;
        nextAnswer = result.answer;
        nextScore = 0;
      } else {
        nextRevealedClues = [...revealedClues, result.next_clue];
      }

      setGuesses(nextGuesses);
      setRevealedClues(nextRevealedClues);
      setStatus(nextStatus);
      setAnswer(nextAnswer);
      setScore(nextScore);
      setInputValue("");

      writeProgress(puzzle.date, {
        puzzleId: puzzle.puzzle_id,
        revealedClues: nextRevealedClues,
        guesses: nextGuesses,
        status: nextStatus,
        answer: nextAnswer,
        score: nextScore,
      });

      if (nextStatus === STATUS.WON || nextStatus === STATUS.LOST) {
        setStreak(recordResult(puzzle.date, nextStatus === STATUS.WON));
      }
    } catch (err) {
      setError(err.message || "Something went wrong submitting that guess.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleShare() {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard API unavailable — silently ignore, the text is still on screen
    }
  }

  if (status === STATUS.LOADING) {
    return (
      <div className="ptm-23g">
        <p className="ptm-23g__loading">Loading today's puzzle…</p>
      </div>
    );
  }

  if (status === STATUS.ERROR) {
    return (
      <div className="ptm-23g">
        <p className="ptm-23g__error">{error}</p>
      </div>
    );
  }

  return (
    <div className="ptm-23g">
      <header className="ptm-23g__header">
        <h1>23 GUESSES</h1>
        <p className="ptm-23g__subtitle">Today's mystery is waiting.</p>
      </header>

      <div className="ptm-23g__meta">
        <span>{puzzle.category}</span>
        <span className="ptm-23g__dot">·</span>
        <span>{puzzle.sport}</span>
        <span className="ptm-23g__dot">·</span>
        <span>
          CLUE {clueIndex + 1} OF {puzzle.total_clues}
        </span>
      </div>

      <ol className="ptm-23g__clues">
        {revealedClues.map((clue, i) => (
          <li key={i} className="ptm-23g__clue">
            <span className="ptm-23g__clue-index">{i + 1}</span>
            {clue}
          </li>
        ))}
      </ol>

      {!isOver && (
        <form className="ptm-23g__form" onSubmit={handleSubmit}>
          <input
            className="ptm-23g__input"
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Your guess"
            disabled={submitting}
            autoFocus
          />
          <button className="ptm-23g__submit" type="submit" disabled={submitting}>
            GUESS
          </button>
        </form>
      )}

      {guesses.length > 0 && (
        <ul className="ptm-23g__guesses">
          {guesses.map((g, i) => (
            <li key={i} className={g.correct ? "is-correct" : "is-wrong"}>
              {g.text}
            </li>
          ))}
        </ul>
      )}

      {isOver && (
        <div className="ptm-23g__result">
          <p className="ptm-23g__result-title">{status === STATUS.WON ? "✓ CORRECT" : "OUT OF CLUES"}</p>
          <p className="ptm-23g__answer">{answer}</p>

          <div className="ptm-23g__stats">
            <div>
              <span className="ptm-23g__stat-value">{guesses.length}</span>
              <span className="ptm-23g__stat-label">GUESSES</span>
            </div>
            <div>
              <span className="ptm-23g__stat-value">{score}</span>
              <span className="ptm-23g__stat-label">SCORE</span>
            </div>
            <div>
              <span className="ptm-23g__stat-value">{streak}</span>
              <span className="ptm-23g__stat-label">STREAK</span>
            </div>
          </div>

          <button className="ptm-23g__share" onClick={handleShare} type="button">
            {copied ? "COPIED" : "SHARE RESULT"}
          </button>
        </div>
      )}

      {error && isOver === false && <p className="ptm-23g__error">{error}</p>}
    </div>
  );
}
