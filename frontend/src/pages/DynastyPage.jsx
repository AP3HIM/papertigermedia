import { useEffect } from "react";
import DynastyGame from "../games/dynasty/DynastyGame";

export default function DynastyPage() {
  useEffect(() => {
    document.title = "Dynasty — Paper Tigers Media";
  }, []);

  return <DynastyGame />;
}
