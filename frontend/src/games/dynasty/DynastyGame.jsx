import { useEffect, useState } from "react";
import { advanceDynasty, newDynastyGame, resolveDynastySituation } from "../../lib/api";
import DecisionScreen from "./DecisionScreen";
import IntroScreen from "./IntroScreen";
import RetrospectiveScreen from "./RetrospectiveScreen";
import SeasonResultScreen from "./SeasonResultScreen";
import SituationScreen from "./SituationScreen";
import { clearSave, readSave, writeSave } from "./storage";
import "./Dynasty.css";

const TOTAL_SEASONS = 10;

const PHASE = {
  INTRO: "intro",
  STARTING: "starting",
  DECIDING: "deciding",
  SIMULATING: "simulating",
  RESULT: "result",
  SITUATION: "situation",
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
  const [pendingSituation, setPendingSituation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const saved = readSave();
    if (saved) {
      setGameState(saved.gameState);
      setDecision(saved.decision);
      setSeasonResult(saved.seasonResult);
      setThreePeat(saved.threePeat || false);
      setGameOverPending(saved.gameOverPending || false);
      setPendingSituation(saved.pendingSituation || null);
      setPhase(saved.phase);
    }
  }, []);

  async function handleStart(city, teamName, philosophy) {
    setPhase(PHASE.STARTING);
    try {
      const data = await newDynastyGame({ city, teamName, philosophy });
      setGameState(data.state);
      setDecision(data.decision);
      setSeasonResult(null);
      setThreePeat(false);
      setGameOverPending(false);
      setPendingSituation(null);
      setPhase(PHASE.DECIDING);

      writeSave({
        phase: PHASE.DECIDING,
        gameState: data.state,
        decision: data.decision,
        seasonResult: null,
        threePeat: false,
        gameOverPending: false,
        pendingSituation: null,
      });
    } catch (err) {
      setError(err.message || "Couldn't start a new dynasty.");
      setPhase(PHASE.ERROR);
    }
  }

  async function handleChoice(chosenOptions) {
    setPhase(PHASE.SIMULATING);
    try {
      const choices = Array.isArray(chosenOptions) ? chosenOptions : [chosenOptions];
      const result = await advanceDynasty({
        state: gameState,
        choices,
      });

      setGameState(result.state);
      setSeasonResult(result.season_result);
      setThreePeat(result.three_peat);
      setDecision(result.next_decision);
      setGameOverPending(result.game_over);
      setPendingSituation(result.pending_situation || null);
      setPhase(PHASE.RESULT);

      writeSave({
        phase: PHASE.RESULT,
        gameState: result.state,
        decision: result.next_decision,
        seasonResult: result.season_result,
        threePeat: result.three_peat,
        gameOverPending: result.game_over,
        pendingSituation: result.pending_situation || null,
      });
    } catch (err) {
      setError(err.message || "Couldn't simulate that season.");
      setPhase(PHASE.ERROR);
    }
  }

  function afterResult() {
    if (pendingSituation) {
      setPhase(PHASE.SITUATION);
      writeSave({
        phase: PHASE.SITUATION,
        gameState,
        decision,
        seasonResult,
        threePeat,
        gameOverPending,
        pendingSituation,
      });
      return;
    }

    const nextPhase = gameOverPending ? PHASE.COMPLETE : PHASE.DECIDING;
    setPhase(nextPhase);

    if (nextPhase === PHASE.COMPLETE) {
      clearSave();
    } else {
      writeSave({ phase: nextPhase, gameState, decision, seasonResult, threePeat, gameOverPending, pendingSituation: null });
    }
  }

  async function handleSituationChoice(option) {
    try {
      const result = await resolveDynastySituation({
        state: gameState,
        situationId: pendingSituation.situation_id,
        choiceId: option.id,
        context: pendingSituation.context,
      });

      setGameState(result.state);
      setPendingSituation(null);

      const nextPhase = gameOverPending ? PHASE.COMPLETE : PHASE.DECIDING;
      setPhase(nextPhase);

      if (nextPhase === PHASE.COMPLETE) {
        clearSave();
      } else {
        writeSave({
          phase: nextPhase,
          gameState: result.state,
          decision,
          seasonResult,
          threePeat,
          gameOverPending,
          pendingSituation: null,
        });
      }
    } catch (err) {
      setError(err.message || "Couldn't resolve that situation.");
      setPhase(PHASE.ERROR);
    }
  }

  function handleContinue() {
    afterResult();
  }

  function handleRestart() {
    clearSave();
    setGameState(null);
    setDecision(null);
    setSeasonResult(null);
    setThreePeat(false);
    setGameOverPending(false);
    setPendingSituation(null);
    setPhase(PHASE.INTRO);
  }

  if (phase === PHASE.ERROR) {
    return (
      <div className="ptm-dynasty">
        <p className="ptm-dynasty__error">{error}</p>
      </div>
    );
  }

  if (phase === PHASE.STARTING) {
    return (
      <div className="ptm-dynasty">
        <p className="ptm-dynasty__loading">Building your franchise…</p>
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
        hotSeat={gameState.hot_seat}
        chemistry={gameState.chemistry}
        pickNumber={decision.pick_number}
        draftClass={gameState.draft_class}
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

  if (phase === PHASE.SITUATION) {
    return (
      <SituationScreen
        city={gameState.city}
        teamName={gameState.team_name}
        seasonNumber={seasonResult ? seasonResult.season_number : gameState.season_number}
        totalSeasons={TOTAL_SEASONS}
        fanSupport={gameState.fan_support}
        hotSeat={gameState.hot_seat}
        chemistry={gameState.chemistry}
        situation={pendingSituation}
        onChoose={handleSituationChoice}
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