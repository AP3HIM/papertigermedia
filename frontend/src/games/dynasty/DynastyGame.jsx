import { useEffect, useState } from "react";
import { advanceDynasty, newDynastyGame } from "../../lib/api";
import DecisionScreen from "./DecisionScreen";
import IntroScreen from "./IntroScreen";
import RetrospectiveScreen from "./RetrospectiveScreen";
import SeasonResultScreen from "./SeasonResultScreen";
import { clearSave, readSave, writeSave } from "./storage";
import "./Dynasty.css";

const TOTAL_SEASONS = 10;

const PHASE = {
  INTRO: "intro",
  DECIDING: "deciding",
  SIMULATING: "simulating",
  RESULT: "result",
  COMPLETE: "complete",
  ERROR: "error",
};

export default function DynastyGame() {
  const [phase, setPhase] = useState(PHASE.INTRO);
  const [gameState, setGameState] = useState(null);
  const [decision, setDecision] = useState(null);
  const [seasonResult, setSeasonResult] = useState(null);
  const [threePeat, setThreePeat] = useState(false);
  const [gameOverPending, setGameOverPending] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const saved = readSave();
    if (saved) {
      setGameState(saved.gameState);
      setDecision(saved.decision);
      setSeasonResult(saved.seasonResult);
      setThreePeat(saved.threePeat || false);
      setGameOverPending(saved.gameOverPending || false);
      setPhase(saved.phase);
    }
  }, []);

  async function handleStart(city, teamName) {
    try {
      const data = await newDynastyGame({ city, teamName });
      setGameState(data.state);
      setDecision(data.decision);
      setSeasonResult(null);
      setThreePeat(false);
      setGameOverPending(false);
      setPhase(PHASE.DECIDING);

      writeSave({
        phase: PHASE.DECIDING,
        gameState: data.state,
        decision: data.decision,
        seasonResult: null,
        threePeat: false,
        gameOverPending: false,
      });
    } catch (err) {
      setError(err.message || "Couldn't start a new dynasty.");
      setPhase(PHASE.ERROR);
    }
  }

  async function handleChoice(option) {
    setPhase(PHASE.SIMULATING);
    try {
      const result = await advanceDynasty({
        state: gameState,
        choiceId: option.id,
        chosenOption: option,
      });

      setGameState(result.state);
      setSeasonResult(result.season_result);
      setThreePeat(result.three_peat);
      setDecision(result.next_decision);
      setGameOverPending(result.game_over);
      setPhase(PHASE.RESULT);

      writeSave({
        phase: PHASE.RESULT,
        gameState: result.state,
        decision: result.next_decision,
        seasonResult: result.season_result,
        threePeat: result.three_peat,
        gameOverPending: result.game_over,
      });
    } catch (err) {
      setError(err.message || "Couldn't simulate that season.");
      setPhase(PHASE.ERROR);
    }
  }

  function handleContinue() {
    const nextPhase = gameOverPending ? PHASE.COMPLETE : PHASE.DECIDING;
    setPhase(nextPhase);

    if (nextPhase === PHASE.COMPLETE) {
      clearSave();
    } else {
      writeSave({ phase: nextPhase, gameState, decision, seasonResult, threePeat, gameOverPending });
    }
  }

  function handleRestart() {
    clearSave();
    setGameState(null);
    setDecision(null);
    setSeasonResult(null);
    setThreePeat(false);
    setGameOverPending(false);
    setPhase(PHASE.INTRO);
  }

  if (phase === PHASE.ERROR) {
    return (
      <div className="ptm-dynasty">
        <p className="ptm-dynasty__error">{error}</p>
      </div>
    );
  }

  if (phase === PHASE.INTRO) {
    return <IntroScreen onStart={handleStart} />;
  }

  if (phase === PHASE.SIMULATING) {
    return (
      <div className="ptm-dynasty">
        <p className="ptm-dynasty__loading">Simulating the season…</p>
      </div>
    );
  }

  if (phase === PHASE.DECIDING) {
    return (
      <DecisionScreen
        city={gameState.city}
        teamName={gameState.team_name}
        seasonNumber={decision.season_number}
        totalSeasons={TOTAL_SEASONS}
        fanSupport={gameState.fan_support}
        pickNumber={decision.pick_number}
        options={decision.options}
        onChoose={handleChoice}
        priorResult={seasonResult}
        roster={gameState.roster}
        depthRating={gameState.depth_rating}
      />
    );
  }

  if (phase === PHASE.RESULT) {
    return (
      <SeasonResultScreen
        city={gameState.city}
        teamName={gameState.team_name}
        totalSeasons={TOTAL_SEASONS}
        result={seasonResult}
        onContinue={handleContinue}
        roster={gameState.roster}
        depthRating={gameState.depth_rating}
      />
    );
  }

  if (phase === PHASE.COMPLETE) {
    return (
      <RetrospectiveScreen
        city={gameState.city}
        teamName={gameState.team_name}
        history={gameState.history}
        roster={gameState.roster}
        depthRating={gameState.depth_rating}
        maxStreak={gameState.max_streak}
        threePeat={threePeat}
        onRestart={handleRestart}
      />
    );
  }

  return null;
}
