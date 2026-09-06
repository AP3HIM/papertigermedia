import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import GamesIndexPage from "./pages/GamesIndexPage";
import PlannedPage from "./pages/PlannedPage";
import TwentyThreeGuessesPage from "./pages/TwentyThreeGuessesPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/games" element={<GamesIndexPage />} />
        <Route path="/games/23-guesses" element={<TwentyThreeGuessesPage />} />
        <Route
          path="/games/dynasty"
          element={
            <PlannedPage
              eyebrow="PLAY"
              title="Dynasty"
              blurb="Build a multi-season sports franchise, live with the consequences of every decision, and watch your own history unfold. In active development."
            />
          }
        />
        <Route
          path="/games/stat-challenge"
          element={
            <PlannedPage
              eyebrow="PLAY"
              title="Stat Challenge"
              blurb="Turn sports statistics into a puzzle — find every player who fits a set of impossible-sounding conditions. Coming after Dynasty."
            />
          }
        />
        <Route
          path="/lab"
          element={
            <PlannedPage
              eyebrow="LAB"
              title="Sports Lab"
              blurb="Simulations, historical experiments, and 'what if' scenarios built on top of the same data powering the games. Planned."
            />
          }
        />
        <Route
          path="/articles"
          element={
            <PlannedPage
              eyebrow="ARCHIVE"
              title="Archive"
              blurb="The original Paper Tigers Media articles, being ported into this rebuild. Planned."
            />
          }
        />
      </Route>
    </Routes>
  );
}
