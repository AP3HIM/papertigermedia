import { Routes, Route } from "react-router-dom";
import Analytics from "./components/Analytics";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import GamesIndexPage from "./pages/GamesIndexPage";
import PlannedPage from "./pages/PlannedPage";
import TwentyThreeGuessesPage from "./pages/TwentyThreeGuessesPage";
import DynastyPage from "./pages/DynastyPage";

import ArticlesIndexPage from "./pages/ArticlesIndexPage";
import ArticleDetailPage from "./pages/ArticleDetailPage";

import PrivacyPage from "./pages/PrivacyPage";
import ContactPage from "./pages/ContactPage";

export default function App() {
  return (
    <>
      <Analytics />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/games" element={<GamesIndexPage />} />
          <Route path="/games/23-guesses" element={<TwentyThreeGuessesPage />} />
          <Route path="/games/dynasty" element={<DynastyPage />} />

          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/contact" element={<ContactPage />} />

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

          <Route path="/articles" element={<ArticlesIndexPage />} />
          <Route path="/articles/:slug" element={<ArticleDetailPage />} />

        </Route>
      </Routes>
    </>
  );
}