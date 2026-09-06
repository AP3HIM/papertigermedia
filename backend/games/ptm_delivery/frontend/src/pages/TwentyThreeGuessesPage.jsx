import { useEffect } from "react";
import TwentyThreeGuesses from "../games/twentyThreeGuesses/TwentyThreeGuesses";

export default function TwentyThreeGuessesPage() {
  useEffect(() => {
    document.title = "23 Guesses — Paper Tigers Media";
  }, []);

  return <TwentyThreeGuesses />;
}
