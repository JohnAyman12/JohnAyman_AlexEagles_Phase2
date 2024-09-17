import React, { useState } from "react";
import axios from "axios";

function App() {
  const [maze, setMaze] = useState(null);
  const [solution, setSolution] = useState(null);
  const [difficulty, setDifficulty] = useState("easy"); // State for selected difficulty

  // Function to generate maze
  const generateMaze = () => {
    console.log("Generating maze with difficulty:", difficulty); // Debugging
    axios
      .get(`http://localhost:5000/generate-maze?difficulty=${difficulty}`)
      .then((response) => {
        setMaze(response.data.maze);
        setSolution(null);
      })
      .catch((error) => console.error("Error generating maze:", error));
  };

  // Function to solve maze
  const solveMaze = () => {
    if (maze) {
      axios
        .post("http://localhost:5000/solve-maze", { maze })
        .then((response) => setSolution(response.data.solution))
        .catch((error) => console.error("Error solving maze:", error));
    }
  };

  const isSolutionPath = (rowIndex, cellIndex) => {
    return (
      solution && solution.some(([x, y]) => x === rowIndex && y === cellIndex)
    );
  };

  // Function to handle difficulty selection
  const handleDifficultyChange = (event) => {
    setDifficulty(event.target.value);
  };

  const getColor = (value) => {
    switch (value) {
      case ".":
        return "green"; // Open path
      case "o":
        return "red"; // Wall
      case "S":
        return "blue"; // Start point
      case "E":
        return "black"; // End point
      // default:
      //   return "yellow";
    }
  };

  return (
    <div>
      <h1>Maze Game</h1>
      <label>Select Difficulty: </label>
      <select value={difficulty} onChange={handleDifficultyChange}>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>

      <button onClick={generateMaze}>Generate Maze</button>
      <button onClick={solveMaze}>Solve Maze</button>

      <div>
        {maze &&
          maze.map((row, rowIndex) => (
            <div key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <span
                  key={cellIndex}
                  style={{
                    margin: "5px",
                    display: "inline-block",
                    width: "20px",
                    height: "20px",
                    backgroundColor: isSolutionPath(rowIndex, cellIndex)
                      ? "yellow"
                      : getColor(cell),
                  }}
                />
              ))}
            </div>
          ))}
      </div>

      <div>
        {solution && <h2>Solution Path: {JSON.stringify(solution)}</h2>}
      </div>
    </div>
  );
}

export default App;
